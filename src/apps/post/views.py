from django.shortcuts import render 
from .forms import PostForm

from django.views.generic import TemplateView
# Create your views here.

class IndexPageView(TemplateView):
    template_name = "index.html"

def create_post(request):
    if request.method == 'Пост':
        form = PostForm(request.POST, request.FILES)
        form.save()            
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form})