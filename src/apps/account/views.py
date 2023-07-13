from typing import Any, Optional
from django.db import models
from django.shortcuts import render, redirect
from .forms import *

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, CreateView, UpdateView, ListView,TemplateView
from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.http import HttpResponse
from .models import User
from django.contrib import messages
from django.views import View
from django.contrib.auth.decorators import login_required
from src.apps.post.models import Post
from src.apps.account.forms import LoginForm, UserRegisterForm, UserUpdateForm
# Create your views here.
from src.apps.account.models import User
from django.db.models import Q


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
                return HttpResponse("Ваш аккаунт не активен")
        return HttpResponse("Такого пользователя не существует или данные неверны")
    

      

def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect("index")

class UsersSearchListView(ListView):
    template_name='users.html'
    model=User
    
    def get_queryset(self):
        search_text=self.request.Get.get('query')
        if search_text:
            search_users=User.objects.filter(username__icontains=search_text)
            return search_users
        return None
    
    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['search_text'] = self.request.Get.get('query')
        return context








@login_required(login_url='login')
def follow(request, pk):
    follow_user = User.objects.get(pk=pk)
    if request.user != follow_user:
        if request.user not in follow_user.followers.all():
            follow_user.followers.add(request.user)
            messages.success(request, f'Вы подписались на {follow_user.username}')
        else:
            messages.info(request, f'Вы уже подписаны на {follow_user.username}')
    else:
        messages.info(request, 'Вы не можете подписаться на самого себя')
    return redirect(reverse_lazy("profile", kwargs={"pk":follow_user.pk}))


@login_required(login_url='login')
def unfollow(request, pk):
    unfollow_user = User.objects.get(pk=pk)
    if request.user != unfollow_user:
        if request.user in unfollow_user.followers.all():
            unfollow_user.followers.remove(request.user)
            messages.success(request, f'Вы отписались от {unfollow_user.username}')
        else:
            messages.info(request, f'Вы не были подписаны на {unfollow_user.username}')
    else:
        messages.info(request, 'Вы не можете отписаться от самого себя')
    return redirect(reverse_lazy("profile", kwargs={"pk":unfollow_user.pk}))


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

  
  
def get_user_profile(request, pk):
    user = User.objects.get(id=pk)
    posts = Post.objects.filter(author=pk)
    context = {
        "user": user,
        "posts": posts,
    }
    return render(request, "profile.html", context)



class UserUpdateProfile(LoginRequiredMixin, UpdateView):
    model = User
    template_name = "edit_profile.html"
    queryset = User.objects.all()
    form_class=UserUpdateForm
    success_url = reverse_lazy("index")


    def get_object(self):
        return self.request.user


def search(request):
    form = SearchForm(request.GET)
    results = []
    if form.is_valid() and form.is_bound:
        query = form.cleaned_data.get('query')
        if query: 
            results = User.objects.filter(Q(username__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query))
    return render(request, 'search.html', {'form': form, 'results': results})