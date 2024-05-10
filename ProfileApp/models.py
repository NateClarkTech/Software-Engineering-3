from django.db import models
from django.contrib.auth.models import User


'''
This is the Profile model, it will be connected to a single user, and hold all of that users profile info.
@W_Farmer
    @user: This will hold the user the profile belongs too
    @profile_picture: This will hold the profile picture of the user
    @personal_info: This will hold the personal info of the user
    @firstName: This will hold the first name of the user
    @lastName: This will hold the last name of the user
    @displayName: This will hold a boolean to tell us if the user wants us to display their name
    @email: This will hold the email of the user
    @displayEmail: This will hold a boolean to tell us if the user wants us to display their email
    @phoneNumber: This will hold the phone number of the user
    @displayNumber: This will hold a boolean to tell us if the user wants us to display their phone number
    @__str__: This will return the username of the user
    
'''
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

    def __str__(self):
        return "Profile: " + self.user.username
    
    

'''
This is the ProfileComment model, will represent a comment on a users profile
@profile: the profile the comment is on
@user: the user who created the comment
@content: the content of the comment
@created_at: the time the comment was created
@__str__: this will return a string that holds the username, and the profile username

'''
class ProfileComment(models.Model):
    profile = models.ForeignKey(Profile, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='profile_comments', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.profile.user.username}'