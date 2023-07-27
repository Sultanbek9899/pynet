from django import forms 
from src.apps.account.models import User
from .models import *
from django.views import View
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
        model = Comment
        fields = ['comments'] 
        widgets={
            'comments': forms.TextInput(attrs={'class': 'form-control form-control-md', 'id': 'message', 'placeholder': 'Enter Comment'})
        }

class RepostForm(forms.Form):
    pass
#     # model=Repost
#     # fields=['repost_post']    
#     # widgets = {
#     #     'repost': forms.TextInput(attrs={'class': 'form-control'}),
    
#     # }
      
      
class UpdatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "description",
            "image",
        ]

class UView(View):
    model = Post
    template_class = "post_update.html"
    form_class = UpdatePostForm

     