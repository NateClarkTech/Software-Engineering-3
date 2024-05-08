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
            'item_image',
            'item_sound',
        ]
        
class NewItemLabelForm(forms.ModelForm):
    class Meta:
        model = ItemLabel
        fields = [
            'label_name'
        ]
