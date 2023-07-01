from django.shortcuts import render, redirect

from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
# Create your views here.

from .forms import *



class IndexPageView(TemplateView):
    template_name = "index.html"


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
        form = AddPostForm()
        return render(request, 'index.html', {'form': form})