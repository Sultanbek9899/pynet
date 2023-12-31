from src.apps.account.models import User
from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment, Repost
from .forms import CommentForm
import datetime
from django.utils import timezone
from django.urls import reverse_lazy
from django.shortcuts import render, redirect

import re
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import FormMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse, JsonResponse
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
    

def extract_hashtags(description):
    return set(tag[1:] for tag in re.findall(r'#\w+', description))

@login_required
def add_post(request):
    if request.method == 'POST':
        form = AddPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            hashtags_str = form.cleaned_data['description']
            hashtags = set(tag[1:] for tag in re.findall(r'#\w+', hashtags_str))
            post.save()
            for tag_name in hashtags:
                hashtag, _ = Hashtag.objects.get_or_create(name=tag_name)
                post.hashtags.add(hashtag)
            return redirect('index')
    else:
        form = AddPostForm()

    context = {'form': form}
    return render(request, 'index.html', context)

        

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
  
@login_required
def add_to_bookmarks(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    request.user.bookmarks.add(post)
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def remove_from_bookmarks(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    request.user.bookmarks.remove(post)
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def get_bookmarks(request):
    bookmarks = request.user.bookmarks.all()
    context = {'bookmarks': bookmarks}
    return render(request, 'bookmarks.html', context)


  

def calculate_rating(post):
    rating = post.comments.count() + ( post.author.followers.count() * 2 ) + (post.likes.count() * 3)
    return rating

  
def recommendations_view(request, hashtag = None):
    if hashtag:
        hashtag_obj = Hashtag.objects.get(name=hashtag)
        posts = Post.objects.filter(hashtags=hashtag_obj)
    else :
        posts = Post.objects.all()

    sorted_posts = sorted(posts, key=calculate_rating, reverse=True)
    context = {
        'posts': sorted_posts
    }
    return render(request, 'recommendations.html', context)


@login_required(login_url='login')
def repost_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.author == request.user:
        return HttpResponse('Вы не можете поделиться своим постом')
    if Repost.objects.filter(user=request.user, reposted_post=post).exists():
        return HttpResponse('Вы уже сделали репост этого поста')
    repost = Repost(user=request.user, reposted_post=post)
    repost.save()
    request.user.posts.add(post)
    request.user.save()
    return redirect('index')



   

