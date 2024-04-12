from .models import *;
from django import forms
from django.contrib.auth.models import User
from datetime import date

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']


# Here we have the profile update form, it allows users to update their profiles, and takes in every possible field
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'profile_picture', 'personal_info', 'firstName', 'lastName', 'displayName',
            'email', 'displayEmail', 'phoneNumber', 'displayNumber',
        ]
        widgets = {
            'personal_info': forms.Textarea(attrs={'rows': 4}),
        }
    # Add Some validation for the graduation year,  https://docs.djangoproject.com/en/5.0/ref/forms/validation/
    
# A profile search form from gpt
class ProfileSearchForm(forms.Form):
    query = forms.CharField(label='Search Profiles', max_length=100)
