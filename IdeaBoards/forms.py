from .models import *;
from django import forms
from django.contrib.auth.models import User

class NewIdeaBoardForm(forms.ModelForm):
    class Meta:
        model = IdeaBoard
        fields = [
            'title', 
            'description'
            ]
        
class NewIdeaBoardItemForm(forms.ModelForm):
    class Meta:
        model = IdeaBoardItem
        fields = [
            'title', 
            'description',
            'board_image',
            'board_sound',
            'note_label',
        ]
        
