# forum/models.py
# Written by gpt
from django.db import models
from django.contrib.auth.models import User

class Page(models.Model):
    title = models.CharField(max_length=100)

class Thread(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    original_poster = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='created_threads')

    # A list of users who have "subscribed" to the thread
    subscribers = models.ManyToManyField(User, related_name='subscribed_threads', blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    # Add other fields
    @property
    def comment_count(self):
        return self.comment.count()


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
    
    

class Like(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('comment', 'user')  # Ensures a user can only like a comment once

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
