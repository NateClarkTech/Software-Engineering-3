from django.db import models
from django.contrib.auth.models import User

"""
* IdeaBoard: A model that represents a board that contains a collection of notes.
"""
class IdeaBoard(models.Model):
    #board details
    title = models.CharField(max_length=64)
    description = models.TextField(blank=True, default='', max_length=128)
    is_public = models.BooleanField(default=False)

    #board creation and update timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return 'Owner:' + self.user.username + " Board:" + self.title + "ID: " + str(self.id) + " Public: " + str(self.is_public)

# Function to upload images to a user's directory
def user_directory_path(instance, filename): 
  
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename> 
    return 'user_{0}/{1}'.format(instance.user.id, filename) 
    

"""
* ItemLabel: A model that represents a label that can be assigned to a note.
"""
class ItemLabel(models.Model):
    #label details
    label_name = models.CharField(max_length=15)
    label_board = models.ForeignKey(IdeaBoard, on_delete=models.CASCADE)
    
    def __str__(self): 
         return self.label_name


"""
* IdeaBoardItem: A model that represents a note that belongs to a board.
* Notes can have text, images, sounds, and be categorized by user-defined labels.
"""
class IdeaBoardItem(models.Model):
    #item details
    title = models.CharField(max_length=64)
    description = models.TextField(blank=True, default='')
    item_image = models.ImageField(upload_to='item_image/', blank=True, null=True)
    item_sound = models.FileField(upload_to='item_sounds/', blank=True, null=True)
    note_label = models.ForeignKey(ItemLabel, on_delete=models.CASCADE, blank=True, null=True) # many-to-one relationship: categorizing notes by user defined labels.
    
    #item creation and update timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey('auth.User', related_name='ideaboarditems', on_delete=models.CASCADE)
    ideaboard = models.ForeignKey(IdeaBoard, related_name='ideaboarditems', on_delete=models.CASCADE)

    def __str__(self):
        return "Board:" + self.ideaboard.title +' user: ' + self.owner.username + ' Item: ' + self.title