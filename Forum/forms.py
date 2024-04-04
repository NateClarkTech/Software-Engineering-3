# forum/forms.py
from django import forms
from .models import Thread, Page, Comment

class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ['title']

class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ['title']



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['content'].widget = forms.Textarea(attrs={'rows': 3})  # Adjust textarea size if needed
        self.fields['content'].label = ''  # Remove label if desired
        self.fields['content'].widget.attrs['placeholder'] = 'Write your comment here...'  # Add placeholder text
