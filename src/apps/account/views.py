from django.shortcuts import render, redirect

from django.views.generic import FormView, CreateView, TemplateView
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.http import HttpResponse

from src.apps.account.forms import LoginForm, UserRegisterForm
# Create your views here.
from src.apps.account.models import User


class LoginView(FormView):
    template_name="login.html"
    form_class = LoginForm

    def form_valid(self, form):
        data = form.cleaned_data # в cleaned_data хранятся данные из форма
        username = data["username"]
        password = data["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(self.request, user)
                return redirect("index")
            else:
                HttpResponse("Ваш аккаунт не активен")
        HttpResponse("Такого пользователя не существует или данные неверны")


# def user_login(request):
#     if request.method == "POST":
#         form  = LoginForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data["username"]
#             password = form.cleaned_data["password"]
#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     return redirect("index")
#                 else:
#                     HttpResponse("Ваш аккаунт не активен")
#             HttpResponse("Такого пользователя не существует или данные неверны")
#     else:
#         form = LoginForm()
#         context = {"form":form}
#         return render(request,"login.html", context)

def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect("index")


# class UserRegisterView(CreateView):
#     template_name = "register.html"
#     form_class = UserRegisterForm
#     model = User 
#     success_url = reverse_lazy('index')


def register_user(request):
    form = UserRegisterForm()
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data["password1"]
            user = User.objects.create(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                first_name=form.cleaned_data["first_name"],
                last_name=form.cleaned_data["last_name"]
            )
            user.set_password(password)
            user.save()
            login(request, user)
            return redirect("index")
    
    context = {'form':form}
    return render(request, 'register.html', context)

