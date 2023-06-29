from django import forms
from django.contrib.auth.forms import UserCreationForm

from src.apps.account.models import User

class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class":"form-control"}),
        label="Логин"
        )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class":"form-control"}),
        label="Пароль"
        )
    

class UserRegisterForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields= ["username", 
                  "first_name", 
                  "last_name",
                  ]
        unique_together = ["username"]