from django import forms 
from src.apps.account.models import User
from .models import *


class AddPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['description', 'image']
        widgets = {
            'description': forms.TextInput(attrs={'class': 'form-control form-control-md', 'id': 'message', 'placeholder': 'Message'}),
            'image': forms.FileInput(attrs={'class': 'form-control', 'id': 'photo-upload', 'hidden': 'true', 'name': 'image', 'style': 'display: none;'}),
        }

class SearchForm(forms.Form):
    query = forms.CharField(label="", max_length=255, required=False)
      
        