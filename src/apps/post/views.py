from src.apps.account.models import User
from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect


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

def search(request):
    form = SearchForm(request.GET)
    results = []
    if form.is_valid() and form.is_bound:
        query = form.cleaned_data.get('query')
        if query: 
            results = User.objects.filter(Q(username__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query))
    return render(request, 'search.html', {'form': form, 'results': results})
    
    

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