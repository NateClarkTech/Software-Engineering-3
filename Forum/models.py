# forum/models.py
# Written by gpt
from django.db import models
from django.contrib.auth.models import User

'''
    The model for the page
    @title: the title of the page
    @get_latest_comment: a method that returns the latest comment in the page
'''
class Page(models.Model):
    title = models.CharField(max_length=100)
    def get_latest_comment(self):
        # Import the Comment model here to avoid circular import issues
        from .models import Comment
        # Fetch the latest comment from any thread in this page
        return Comment.objects.filter(thread__page=self).order_by('-created_at').first()


''' 
    The model that will represent a thread in the forum
    @page: the page the thread is on
    @title: the title of the thread
    @original_poster: the user who created the thread
    @subscribers: a list of users who have "subscribed" to the thread
    @created_at: the time the thread was created
    @latest_comment_time: the time of the latest comment in the thread
    @latest_comment_username: the username of the user who made the latest comment
    @comment_count: a property that returns the number of comments in the thread
'''
class Thread(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    original_poster = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='created_threads')

    # A list of users who have "subscribed" to the thread
    subscribers = models.ManyToManyField(User, related_name='subscribed_threads', blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    # redundant code for performence, and so VS code doesnt yell at me
    latest_comment_time = models.DateTimeField(null=True, blank=True)
    latest_comment_username = models.CharField(max_length=100, null=True, blank=True)
    
    # Add other fields
    @property
    def comment_count(self):
        # This works
        return self.comment.count()


'''
    The model that will represent a comment in the forum
    @thread: the thread the comment is on
    @user: the user who created the comment
    @content: the content of the comment
    @created_at: the time the comment was created
    @last_edited: the time the comment was last edited
    @likes: a list of users who have liked the comment
    @parent: the parent comment, if there is one, This is for the reply system
    @like_count: a property that returns the number of likes the comment has
    
'''
class Comment(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name='comment')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    testtext = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    # Optional "last eddited" field
    last_edited = models.DateTimeField(null=True, blank=True)
    # likes
    likes = models.ManyToManyField(User, related_name='liked_comments', blank=True)
    
    # Parent comment, if there is one. For the reply system. 
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    
    # count the number of likes
    @property
    def like_count(self):
        return self.likes.count()
    
    
'''
    The model that will represent a like on a comment
    @comment: the comment that was liked
    @user: the user who liked the comment
    @created_at: the time the like was created
    
'''
class Like(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('comment', 'user')  # Ensures a user can only like a comment once


'''
    The model that will represent a notification 
    @notification_type: the type of notification. Can be LIKE, COMMENT, or REPLY
    @to_user: the user the notification is for
    @from_user: the user who caused the notification
    @thread: the thread the notification is about
    @comment: the comment the notification is about
    @date: the time the notification was created
    @is_read: a boolean that represents if the notification has been read
'''
class Notification(models.Model):
    # Types of notifications
    LIKE = 1
    COMMENT = 2
    REPLY = 3
    NOTIFICATION_TYPES = (
        (LIKE, 'Like'),
        (COMMENT, 'Comment'),
        (REPLY, 'Reply'),
    )

    # Notification fields
    notification_type = models.PositiveSmallIntegerField(choices=NOTIFICATION_TYPES)
    to_user = models.ForeignKey(User, related_name='notifications', on_delete=models.CASCADE)
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    thread = models.ForeignKey('Thread', on_delete=models.CASCADE, related_name='notifications', null=True, blank=True)
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE, related_name='+', null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
