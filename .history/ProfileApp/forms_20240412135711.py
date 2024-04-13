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
            'profile_picture', 'personal_info', 'dorm_preferences', 'major',
            'graduation_year', 'new_student', 'current_student', 'hometown', 'likes', 'homestate', 'highschool', 'looking_for_roommate',
            'email', 'phone_number', 'snapchat', 'instagram'
        ]
        widgets = {
            'personal_info': forms.Textarea(attrs={'rows': 4}),
            'looking_for_roommate': forms.CheckboxInput(),
            'new_student': forms.CheckboxInput(),
        }
    # Add Some validation for the graduation year,  https://docs.djangoproject.com/en/5.0/ref/forms/validation/
    def clean_graduation_year(self):
        graduation_year = self.cleaned_data.get('graduation_year')
        if graduation_year:
            current_year = date.today().year
            if graduation_year < current_year - 10 or graduation_year > current_year + 10:
                raise forms.ValidationError("Invalid graduation year.")
        return graduation_year

# A profile search form from gpt
class ProfileSearchForm(forms.Form):
    query = forms.CharField(label='Search Profiles', max_length=100)
