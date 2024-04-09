# forum/models.py
# Written by gpt
from django.db import models
from django.contrib.auth.models import User

class Page(models.Model):
    title = models.CharField(max_length=100)

class Thread(models.Model):
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
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
