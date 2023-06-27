from django.shortcuts import render, redirect

from django.views.generic import FormView
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse

from src.apps.account.forms import LoginForm
# Create your views here.


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