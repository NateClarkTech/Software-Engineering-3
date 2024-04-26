from django.db import models
from django.contrib.auth.models import User

class IdeaBoard(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(blank=True, default='', max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return 'Board:' + self.user.username + " " + self.title
    
class IdeaBoardItem(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey('auth.User', related_name='ideaboarditems', on_delete=models.CASCADE)
    ideaboard = models.ForeignKey(IdeaBoard, related_name='ideaboarditems', on_delete=models.CASCADE)
    
    def __str__(self):
        return 'Title: ' + self.ideaboard.title + ' Item: ' + self.title