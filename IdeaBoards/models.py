from django.db import models
from django.contrib.auth.models import User

# @Bilge_AKYOL : ItemLabel class;  item_iamge, item_sound, note_label in IdeaBoardItem

class IdeaBoard(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField(blank=True, default='', max_length=128)
    is_public = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return 'Board:' + self.user.username + " " + self.title


def user_directory_path(instance, filename): 
  
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename> 
    return 'user_{0}/{1}'.format(instance.user.id, filename) 
    

class ItemLabel(models.Model):
    label_name = models.CharField(max_length=15)
    label_board = models.ForeignKey(IdeaBoard, on_delete=models.CASCADE)
    def __str__(self): 
         return self.label_name

class IdeaBoardItem(models.Model):
    title = models.CharField(max_length=64)
    label = models.TextField(blank=True, default='')
    description = models.TextField(blank=True, default='')
    item_image = models.ImageField(upload_to='item_image/', blank=True, null=True)
    item_sound = models.FileField(upload_to='item_sounds/', blank=True, null=True)
    note_label = models.ForeignKey(ItemLabel, on_delete=models.CASCADE, blank=True, null=True) # many-to-one relationship: categorizing notes by user defined labels.
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey('auth.User', related_name='ideaboarditems', on_delete=models.CASCADE)
    ideaboard = models.ForeignKey(IdeaBoard, related_name='ideaboarditems', on_delete=models.CASCADE)

    def __str__(self):
        return 'Title: ' + self.ideaboard.title + ' Item: ' + self.title