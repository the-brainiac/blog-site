from django import forms
from .models import Blog, Comment

class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea, required=True, max_length=500, min_length=3, strip=True)

class CreateForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'description', 'thumbnail', 'body']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'create-blog-input'}),
            'description': forms.TextInput(attrs={'class': 'create-blog-input'}),
        }