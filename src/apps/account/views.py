from typing import Any
from django.core.paginator import _SupportsPagination
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, CreateView, UpdateView, ListView
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from account.models import User, Follow
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

    
@login_required(login_url='login')
def profile(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = User.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=pk)
    user_post_length = len(user_posts)

    follower = request.user.username
    user = pk

    if Follow.objects.filter(follower=follower, following=user).first():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'

    user_followers = len(Follow.objects.filter(following=pk))
    user_following = len(Follow.objects.filter(follower=pk))

    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_length': user_post_length,
        'button_text': button_text,
        'user_followers': user_followers,
        'user_following': user_following,
    }
    return render(request, 'profile.html', context)

@login_required(login_url='login')
def follow(request):
    if request.method == 'POST':
        follower = request.POST['follower']
        user = request.POST['user']

        if Follow.objects.filter(follower=follower, following=user).first():
            delete_follower = Follow.objects.get(follower=follower, user=user)
            delete_follower.delete()
            return redirect('/profile/'+user)
        else:
            new_follower = Follow.objects.create(follower=follower, following=user)
            new_follower.save()
            return redirect('/profile/'+user)
    else:
        return redirect('/')

