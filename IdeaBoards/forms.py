from .models import *;
from django import forms
from django.contrib.auth.models import User

class NewIdeaBoardForm(forms.ModelForm):
    class Meta:
        model = IdeaBoard
        fields = [
            'title', 
            'description',
            ]
        
class NewIdeaBoardItemForm(forms.ModelForm):
    class Meta:
        model = IdeaBoardItem
        fields = [
            'title', 
            'description',
            'item_image',
            'item_sound',
            'note_label',
        ]
        

# Bilge: to add labels via the create label button
class NewItemLabelForm(forms.ModelForm):
    class Meta:
        model = ItemLabel
        fields = [
            'label_name',
        ]


# Wes, adapted by Bilge: Form for creating a new comment
class CommentForm(forms.ModelForm):
    # Content field with a textarea widget
    content = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'comment-form-textarea',
        'placeholder': 'Write your comment here...',
        'rows': 4
    }))

    class Meta:
        model = BoardComment
        fields = ['content']


    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['content'].widget = forms.Textarea(attrs={'rows': 3})  # Adjust textarea size if needed
        self.fields['content'].label = ''  # Remove label if desired
        self.fields['content'].widget.attrs['placeholder'] = 'Write your comment here...'  # Add placeholder text