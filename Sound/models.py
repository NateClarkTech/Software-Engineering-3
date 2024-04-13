from django.db import models

# Create your models here.

#similar to VisualLabel
class SoundLabel(models.Model):
    label_name = models.CharField(max_length=15)
    def __str__(self): 
         return self.label_name

#similar to VisualNote
class SoundNote(models.Model):
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    note_title = models.CharField(max_length=30)
    note_description = models.CharField(max_length=1200) # around 500-600 words
    note_label = models.ForeignKey(SoundLabel, on_delete=models.CASCADE, blank=True, null=True) # many-to-one relationship: categorizing notes by user defined labels.
    created_at = models.DateTimeField(auto_now_add=True)