from django.db import models

# Create your models here.

class IdeaBoard(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey('auth.User', related_name='ideaboards', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title2
    
class IdeaBoardItem(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey('auth.User', related_name='ideaboarditems', on_delete=models.CASCADE)
    ideaboard = models.ForeignKey(IdeaBoard, related_name='ideaboarditems', on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title