from django.shortcuts import render 
from .forms import PostForm
from .models import Post

from django.views.generic import TemplateView
# Create your views here.

# class IndexPageView(TemplateView):
#     template_name = "index.html"

# def home(request):
#     posts = Post.objects.all()
#     return render(request, 'index.html', {'posts': posts})

# def create_post(request):
#     if request.method == 'Пост':
#         form = PostForm(request.POST, request.FILES)
#         form.save()            
#     else:
#         form = PostForm()
#     return render(request, 'create_post.html', {'form': form})

# def send_post(request):
#     if request.method == 'POST':
#         message = request.POST.get('message')
#         return render(request, 'myapp/index.html', {'message': message})
#     return render(request, 'myapp/index.html')



class IndexPageView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)    
        context['posts'] = Post.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        view = IndexPageView.as_view(template_name='create_post.html')
        if view.method == 'POST':
            message = request.POST.get('message')
            return render(request, 'index.html', {'message': message})
        return render(request, 'index.html', {'form': form})