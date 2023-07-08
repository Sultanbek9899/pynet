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
                 "email",
                  "first_name", 
                  "last_name",
                  ]
        unique_together = ["username"]

class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = (
            "avatar",
            "email",
            "first_name",
            "last_name",
            "birthday",
            "is_private",
            )
        widgets = {
            "avatar": forms.FileInput(
                attrs={"class":"form-control"}
            ),
            "email": forms.EmailInput(
                attrs={"class":"form-control"}
            ), 
            "first_name": forms.TextInput(
                attrs={"class":"form-control"}
            ),
            "last_name": forms.TextInput(
                attrs={"class":"form-control"}
            ),
            "birthday": forms.DateInput(
                attrs ={"class":"form-control", "type":"date"},
                format=("%Y-%m-%d")
            ),
            "is_private": forms.CheckboxInput(
                attrs={
                    "class":"form-check-input",
                    "type":"checkbox"
                }
            ),
        }

