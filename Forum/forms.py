from django import forms
from .models import Thread, Page, Comment


#@W_Farmer

# Form for creating a new thread
class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ['title']

# Form for creating a new page
class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ['title']


# Form for creating a new comment
class CommentForm(forms.ModelForm):
    # Content field with a textarea widget
    content = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'comment-form-textarea',
        'placeholder': 'Write your comment here...',
        'rows': 4
    }))

    class Meta:
        model = Comment
        fields = ['content']


    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['content'].widget = forms.Textarea(attrs={'rows': 3})  # Adjust textarea size if needed
        self.fields['content'].label = ''  # Remove label if desired
        self.fields['content'].widget.attrs['placeholder'] = 'Write your comment here...'  # Add placeholder text
