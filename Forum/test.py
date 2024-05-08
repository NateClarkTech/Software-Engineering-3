from django.test import TestCase
from django.contrib.auth.models import User
from .models import Page, Thread, Comment, Notification
from .forms import CommentForm, ThreadForm, PageForm
from django.urls import reverse

class ForumTestCase(TestCase):
    def setUp(self):    
        # Create a user
        self.user = User.objects.create_user(username='john', password='doepass')
        # Create a page
        self.page = Page.objects.create(title='Sample Page')
        # Create a thread
        self.thread = Thread.objects.create(title='Sample Thread', page=self.page, original_poster=self.user)
        # Create a comment
        self.comment = Comment.objects.create(content='Sample comment', user=self.user, thread=self.thread)

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


