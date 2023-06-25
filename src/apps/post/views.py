from django.shortcuts import render, redirect
from django.http import HttpResponse
from src.apps.post.models  import Post, Category, Comment
from .forms import CommentForm

def get_categories(request):
    categories=Category.objects.all()
    context1={
        'categories':categories
    }
    return render(request, 'categories.html', context=context1) 

def get_posts(request):
    posts=Post.objects.all()
    context={
        "posts":posts
    }
    return render(request, 'post_list.html',context=context)

def index(request):
    return render(request, 'index.html')

def create_comment(request, post_id):
    post = Post.objects.get(id=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data['content']
            Comment.objects.create(post=post, content=content)
            return redirect('post_detail', post_id=post_id)
    else:
        form = CommentForm()
    return render(request, 'create_comment.html', {'form': form})



