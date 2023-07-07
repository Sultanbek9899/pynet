from typing import Any
from django.http import HttpResponseRedirect
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comments, Likes
from .forms import CommentForm
import datetime
from django.utils import timezone
from django.urls import reverse
from django.views.generic import TemplateView, ListView
from django.views.generic.edit import FormMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CommentForm
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



def create_comment(request, post_id):
    body = request.POST['body']
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            # comment.created_on = timezone.now()  
            comment.save()
            return redirect('index')
    else:
        comments = Comments.objects.filter(post=post).order_by('-created_at')
        form=CommentForm()
        context = {
            'form': form,
            'comments':comments,
            'post':post,
            }
        # return render(request, 'index')

# def reply_to_comment(request, comment_id):
#     parent_comment = get_object_or_404(Comments, id=comment_id)

#     if request.method == 'POST':
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.user = request.user
#             comment.parent_comment = parent_comment
#             # comment.created_on = timezone.now()  
#             comment.save()
#             return redirect('index', comment_id=comment.id)
#     else:
#         form = CommentForm()

#     context = {'form': form}
#     return render(request, 'reply_to_comment.html', context)


    
def like_post(request, post_id):
    user=request.user
    post = get_object_or_404(Post, pk=post_id)
    post.likes.add(request.user)
    current_likes=post.likes
    liked=Likes.objects.filter(user=user, post=post).count
    if not liked:
        liked=Likes.objects.create(user=user, post=post)
        current_likes +=1
    else:
        liked=Likes.objects.filter(user=user, post=post).delete()
        current_likes-=1
    post.likes=current_likes
    post.save()
    return redirect('index', post_id=post_id)
    # return HttpResponseRedirect(reverse('post_details',args=[post_id]))

def like_comment(request, comment_id):
    user=request.user
    comment = get_object_or_404(Comments, pk=comment_id)
    comment.likes.add(request.user)
    current_likes=comment.likes
    liked=Comments.objects.filter(user=user, comment=comment).count
    if not liked:
        liked=Comments.objects.create(user=user, comment=comment)
        current_likes +=1
    else:
        liked=Comments.objects.filter(user=user, comment=comment).delete()
        current_likes-=1
    # comment.likes=current_likes
    # comment.save()
    return redirect('index')

# def display_comments_and_likes(comment,like):
#     comment_timestamp = comment.created_at.timestamp()
#     like_timestamp = like.created_at.timestamp()
#     comment_time_ago = get_time_ago(comment_timestamp, 'Комментарий')
#     comment_like_time_ago = get_time_ago(like_timestamp, 'Нравится')
#     post_like_time_ago = get_time_ago(like_timestamp, 'Нравится')
#     print(f"Время создания комментария: {comment_time_ago}")
#     print(f"Время создания лайка комментария: {comment_like_time_ago}")
#     print(f"Время создания лайка поста: {post_like_time_ago}")

# def get_time_ago(timestamp, entity_type):
#     current_time = timezone.now().timestamp()
#     time_difference = current_time - timestamp

#     minutes = int(time_difference / 60)
#     hours = int(minutes / 60)
#     days = int(hours / 24)
#     weeks = int(days / 7)
#     years = int(days / 365)

#     if minutes == 0:
#         return f'Только что {entity_type}'
#     elif hours == 0:
#         return f'{minutes} минут назад {entity_type}'
#     elif days == 0:
#         return f'{hours} часов назад {entity_type}'
#     elif weeks == 0:
#         return f'{days} дней назад {entity_type}'
#     elif years == 0:
#         return f'{weeks} недель назад {entity_type}'
#     else:
#         return f'{years} лет назад {entity_type}'

