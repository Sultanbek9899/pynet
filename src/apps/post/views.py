from django.shortcuts import render

from django.views.generic import TemplateView
# Create your views here.

from src.apps.account.models import User 
from src.apps.post.models import Post


class IndexPageView(TemplateView):
    template_name = "index.html"


def get_feed(request):

    try: 
        user = request.user
        following = user.followings.all()
        news = Post.objects.filter(author__in=following).order_by('-created_at')
        return render(request, 'index.html', {'news': news})
    
    except AttributeError: 
        return render(request, 'index.html')