from typing import Any
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, CreateView, UpdateView, ListView
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from .models import User
from django.contrib import messages
from django.views import View
from django.contrib.auth.decorators import login_required
from src.apps.post.models import Post
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
        context['search_text']=self.request.Get.get('query')
        return context
    
# class FollowUser(LoginRequiredMixin, View):


#     def get(request, user_pk):
#         following=request.user
#         follower=get_object_or_404(User, pk=user_pk)
#         if following not in follower.followers.all():
#             Follow.objects.create(
#                 follower=follower,
#                 following=following
#             )
#             return redirect('index')
    
# class Unfollow(LoginRequiredMixin, View):

#     def get(request, user_pk):
#         following=request.user
#         follow=Follow.objects.get(
#             following=following,
#             follower__id=user_pk,
#         )
#         follow.delete()
#         return redirect('index')

    
# @login_required(login_url='login')
# def profile(request, pk):
#     user_object = User.objects.get(username=pk)
#     user_profile = User.objects.get(user=user_object)
#     user_posts = Post.objects.filter(user=pk)
#     user_post_length = len(user_posts)

#     follower = request.user.username
#     user = pk

#     if Follow.objects.filter(follower=follower, following=user).first():
#         button_text = 'Unfollow'
#     else:
#         button_text = 'Follow'

#     user_followers = len(Follow.objects.filter(following=pk))
#     user_following = len(Follow.objects.filter(follower=pk))

#     context = {
#         'user_object': user_object,
#         'user_profile': user_profile,
#         'user_p




@login_required(login_url='login')
def follow(request, pk):
    profile = User.objects.get(pk=pk).profile
    if request.user.profile != profile:
        if profile not in request.user.profile.follows.all():
            request.user.profile.follows.add(profile)
            messages.success(request, f'Вы подписались на {profile.user.username}')
        else:
            messages.info(request, f'Вы уже подписаны на {profile.user.username}')
    else:
        messages.info(request, 'Вы не можете подписаться на самого себя')
    return redirect('index')

@login_required(login_url='login')
def unfollow(request, pk):
    profile = User.objects.get(pk=pk).profile
    if request.user.profile != profile:
        if profile in request.user.profile.follows.all():
            request.user.profile.follows.remove(profile)
            messages.success(request, f'Вы отписались от {profile.user.username}')
        else:
            messages.info(request, f'Вы не были подписаны на {profile.user.username}')
    else:
        messages.info(request, 'Вы не можете отписаться от самого себя')
    return redirect('index')




