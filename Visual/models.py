from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class VisualLabel(models.Model):
    label_name = models.CharField(max_length=15)
    def __str__(self): 
         return self.label_name # saving the label objects as the user named them

class VisualNote(models.Model):
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    note_title = models.CharField(max_length=30)
    note_description = models.CharField(max_length=1200) # around 500-600 words
    note_label = models.ForeignKey(VisualLabel, on_delete=models.CASCADE, blank=True, null=True) # many-to-one relationship: categorizing notes by user defined labels.
    note_image = models.ImageField(upload_to="images/", default=None, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)