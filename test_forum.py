from django.test import TestCase
from django.contrib.auth.models import User
from Forum.models import *
from Forum.forms import CommentForm, ThreadForm, PageForm
from django.urls import reverse


class ForumTestCase(TestCase):
    
    def setUp(self):
        # Setting up users
        self.user = User.objects.create_user(username='john', password='doepass')
        self.admin = User.objects.create_user(username='admin', password='adminpass', is_superuser=True)
        
        # Setting up pages and threads
        self.page = Page.objects.create(title='Sample Page')
        self.thread = Thread.objects.create(title='Sample Thread', page=self.page, original_poster=self.user)
        self.comment = Comment.objects.create(content='Sample comment', user=self.user, thread=self.thread)
        
        # Log in the user for each test
        self.client.login(username='john', password='doepass')

    def create_comment(self, thread, content='A test comment', user=None):
        return Comment.objects.create(content=content, thread=thread, user=user if user else self.user)
    
    def test_thread_list_view(self):
        self.client.login(username='john', password='doepass')
        url = reverse('thread_list', kwargs={'page_id': self.page.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'thread_list.html')
        self.assertIn('threads', response.context)
    
    def test_thread_detail_view(self):
        self.client.login(username='john', password='doepass')
        url = reverse('thread_detail', kwargs={'thread_id': self.thread.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'thread_details.html')
        self.assertIn('comments', response.context)


    def test_create_comment_post(self):
        self.client.login(username='john', password='doepass')
        url = reverse('create_comment', kwargs={'thread_id': self.thread.pk})
        response = self.client.post(url, {
            'content': 'New comment'
        })
        self.assertEqual(response.status_code, 302)  # Redirect expected
        self.assertTrue(Comment.objects.filter(content='New comment').exists())
    
    def test_mark_notification_as_read(self):
        self.client.login(username='john', password='doepass')
        notification = Notification.objects.create(notification_type=1, to_user=self.user, from_user=self.user, thread=self.thread, comment=self.comment)
        url = reverse('mark_notification_as_read', kwargs={'notification_id': notification.pk})
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        notification.refresh_from_db()
        self.assertTrue(notification.is_read)
        
        
        def test_thread_list_pagination_and_content(self):
            # Create additional threads to test pagination
            for _ in range(15):
                Thread.objects.create(title='More Threads', page=self.page, original_poster=self.user)

            response = self.client.get(reverse('thread_list', kwargs={'page_id': self.page.id}))
            self.assertEqual(response.status_code, 200)
            self.assertTrue(len(response.context['threads']) <= 10)  # Pagination limit
            
        def test_thread_detail_with_comments(self):
            comment = self.create_comment(self.thread, 'Hello world')
            response = self.client.get(reverse('thread_detail', kwargs={'thread_id': self.thread.id}))
            self.assertEqual(response.status_code, 200)
            self.assertIn(comment, response.context['comments'])


    def test_create_comment_valid(self):
        response = self.client.post(reverse('create_comment', kwargs={'thread_id': self.thread.id}), {
            'content': 'Another test comment'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Comment.objects.filter(content='Another test comment').exists())
        
        
    def test_edit_comment_permission_denied(self):
        # Log out any currently logged-in user
        self.client.logout()

        # Log in as another user who does not own the comment
        another_user = User.objects.create_user('jane', 'janepass')
        self.client.login(username='jane', password='janepass')

        # Try to edit the comment
        response = self.client.post(reverse('edit_comment', kwargs={'comment_id': self.comment.id}), {
            'content': 'Edited Comment'
        })

        # Check the response; expecting a redirect or forbidden
        self.assertIn(response.status_code, [403, 302])

        # Verify that the content hasn't changed
        self.comment.refresh_from_db()
        self.assertNotEqual(self.comment.content, 'Edited Comment')

        
    def test_edit_comment_valid(self):
        self.client.login(username='john', password='doepass')
        response = self.client.post(reverse('edit_comment', kwargs={'comment_id': self.comment.id}), {
            'content': 'Edited Comment'
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.get(id=self.comment.id).content, 'Edited Comment')

    def test_notification_mark_as_read(self):
        # Create a notification and ensure it is initially unread
        notification = Notification.objects.create(notification_type=Notification.COMMENT, to_user=self.user, from_user=self.admin, thread=self.thread, comment=self.comment, is_read=False)

        # Send POST request to the mark as read endpoint
        self.client.post(reverse('mark_notification_as_read', kwargs={'notification_id': notification.id}))

        # Refresh the notification object from the database
        notification.refresh_from_db()

        # Check if the notification is now marked as read
        self.assertTrue(notification.is_read)



    def test_create_page_as_superuser(self):
        self.client.login(username='admin', password='adminpass')
        response = self.client.post(reverse('create_page'), {'title': 'New Admin Page'})
        self.assertEqual(response.status_code, 302)  # Expect redirection to 'forum_home' or another success page
        self.assertTrue(Page.objects.filter(title='New Admin Page').exists())

    def test_create_page_as_regular_user(self):
        response = self.client.post(reverse('create_page'), {'title': 'Unauthorized Page'})
        self.assertNotEqual(response.status_code, 302)  # Not allowed to create page, check for failure status
        self.assertFalse(Page.objects.filter(title='Unauthorized Page').exists())


    def test_delete_comment_by_author(self):
        comment_id = self.comment.id
        response = self.client.post(reverse('delete_comment', kwargs={'comment_id': comment_id}))
        self.assertEqual(response.status_code, 302)  # Expect redirection after deletion
        self.assertFalse(Comment.objects.filter(id=comment_id).exists())

    def test_delete_comment_by_non_author(self):
        self.client.logout()
        self.client.login(username='jane', password='janepass')
        comment_id = self.comment.id
        response = self.client.post(reverse('delete_comment', kwargs={'comment_id': comment_id}))
        self.assertEqual(response.status_code, 403)  # Access should be forbidden
        self.assertTrue(Comment.objects.filter(id=comment_id).exists())  # Comment should still exist



    #def test_like_comment(self):
    #    self.client.logout()
    #    self.client.login(username='jane', password='janepass')
    #    response = self.client.post(reverse('like_comment', kwargs={'comment_id': self.comment.id}))
    #    self.assertEqual(response.status_code, 302)  # Expect redirection after liking a comment
    #    self.assertTrue(self.user in self.comment.likes.all())  # Check if the user's like is recorded

    def test_like_own_comment(self):
        response = self.client.post(reverse('like_comment', kwargs={'comment_id': self.comment.id}))
        self.assertEqual(response.status_code, 403)  # User should not be able to like their own comment
        self.assertFalse(self.user in self.comment.likes.all())  # Like should not be recorded
        
        
        
    def test_subscribe_to_thread(self):
        response = self.client.post(reverse('subscribe_to_thread', kwargs={'thread_id': self.thread.id}))
        self.assertEqual(response.status_code, 302)  # Expect redirection after subscribing
        self.assertTrue(self.user in self.thread.subscribers.all())  # User should be in the list of subscribers

    def test_unsubscribe_from_thread(self):
        self.thread.subscribers.add(self.user)  # First, add the user
        response = self.client.post(reverse('unsubscribe_from_thread', kwargs={'thread_id': self.thread.id}))
        self.assertEqual(response.status_code, 302)  # Expect redirection after unsubscribing
        self.assertFalse(self.user in self.thread.subscribers.all())  # User should no longer be subscribed

