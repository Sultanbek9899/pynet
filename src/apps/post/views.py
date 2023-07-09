from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect

from django.views.generic import TemplateView, ListView
from django.views.generic.edit import FormMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404

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
