from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment
from .forms import CommentForm
import datetime
from django.utils import timezone
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import FormMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

from .forms import *

class IndexView(LoginRequiredMixin,FormMixin, ListView):
    form_class = AddPostForm
    model = Post
    success_url = "index"
    template_name="index.html"

    def form_valid(self, form, *args, **kwargs):    
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        return super().form_valid(form)
    
    def get_queryset(self) -> QuerySet[Any]:
        user = self.request.user
        following = user.followings.all()
        posts = Post.objects.filter(
            Q(author__in=following) | Q(author=user)
            ).order_by('-created_at')
        return posts
    

@login_required
def add_post(request):
    if request.method == 'POST':
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('index')
    else: 
        redirect("index")

<<<<<<< HEAD
   

def calculate_rating(post):
    rating = post.comments.count() + post.author.followers.count() * 2
    return rating

def recommendations_view(request):
    posts = Post.objects.all()
    sorted_posts = sorted(posts, key=calculate_rating, reverse=True)
    context = {
        'posts': sorted_posts
    }
    return render(request, 'recommendations.html', context)
    
        
=======
@login_required
def post_details(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(post=post).order_by('-created_at')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect(reverse_lazy('post_details', kwargs={"pk":pk}))
    else:
        form = CommentForm()
        context = {
            'post': post,
            'comments': comments,
            'form': form,
        }

        return render(request, 'post_details.html', context)

@login_required(login_url='login')
def like_post(request, post_id):
    user = request.user
    post = get_object_or_404(Post, pk=post_id)
    current_likes = post.likes.count()
    if user not in post.likes.all():
        post.likes.add(user)
        current_likes += 1
    else:
        post.likes.remove(user)
        current_likes -= 1
    post.save()
    previous_url = request.META.get('HTTP_REFERER')
    return redirect(previous_url)


@login_required(login_url='login')
def like_comment(request, comment_id):
    user = request.user
    comment = get_object_or_404(Comment, pk=comment_id)

    if user not in comment.likes.all():
        comment.likes.add(user)
    else: 
        comment.likes.remove(user)
    comment.save()
    return redirect('post_details')
>>>>>>> 11aaa4ddb8d41ac14574cd0fa7e2124e6db595c1
