
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# Here is the profile model, it will be conected to a single user, and hold all of that users profile info. 
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Profile picture, that is stored in the profile pictures field, and gives us a default image
    profile_picture = models.ImageField(upload_to='profile_pics', default='profile_pics/default.png')
    personal_info = models.TextField(max_length=500, blank=True)
    
    
    # School info
    dorm_preferences = models.CharField(max_length=100, blank=True)
    major = models.CharField(max_length=100, blank=True)
    graduation_year = models.IntegerField(blank=True, null=True)
    current_student = models.BooleanField(default=True)

    # Adding in extra stuff about the user
    likes = models.CharField(max_length=100, blank=True)
    hometown = models.CharField(max_length=100, blank=True)
    homestate = models.CharField(max_length=100, blank=True)
    highschool = models.CharField(max_length=100, blank=True)
    looking_for_roommate = models.BooleanField(default=False)
    # Contact info
    email = models.EmailField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=10, blank=True)
    snapchat = models.CharField(max_length=100, blank=True)
    instagram = models.CharField(max_length=100, blank=True)
    
    #New or returning student
    new_student = models.BooleanField(default=False)