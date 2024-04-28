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


def user_directory_path(instance, filename): 
  
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename> 
    return 'user_{0}/{1}'.format(instance.user.id, filename) 
    
class IdeaBoardItem(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey('auth.User', related_name='ideaboarditems', on_delete=models.CASCADE)
    ideaboard = models.ForeignKey(IdeaBoard, related_name='ideaboarditems', on_delete=models.CASCADE)
    board_image = models.ImageField(upload_to='board_image', height_field="500", width_field="500", max_length=100, blank=True)

    def __str__(self):
        return 'Title: ' + self.ideaboard.title + ' Item: ' + self.title