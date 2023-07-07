from django import forms 
from src.apps.account.models import User
from .models import *
from .models import Post, Comments

class AddPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['description', 'image']
        widgets = {
            'description': forms.TextInput(attrs={'class': 'form-control form-control-md', 'id': 'message', 'placeholder': 'Message'}),
            'image': forms.FileInput(attrs={'class': 'form-control', 'id': 'photo-upload', 'hidden': 'true', 'name': 'image', 'style': 'display: none;'}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['body'] 
        widgets={
            'body': forms.TextInput(attrs={'class': 'form-control form-control-md', 'id': 'message', 'placeholder': 'Enter Comment'})
        }
      
        