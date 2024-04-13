
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# Here is the profile model, it will be conected to a single user, and hold all of that users profile info. 
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Profile picture, that is stored in the profile pictures field, and gives us a default image
    profile_picture = models.ImageField(upload_to='profile_pics', default='profile_pics/default.png')
    personal_info = models.TextField(max_length=500, blank=True)

    # Contact info
    firstName = models.TextField(max_length=25, blank=True)
    lastName = models.TextField(max_length=25, blank=True)
    displayName = models.BooleanField(default=False)
    email = models.EmailField(max_length=100, blank=True)
    displayEmail = models.BooleanField(default=False)
    phoneNumber = models.CharField(max_length=10, blank=True)
    displayNumber = models.BooleanField(default=False)