from django.urls import path

from src.apps.post import views
from src.apps.post.views import add_post

urlpatterns = [
    # path('', views.IndexPageView.as_view( ), name="index"),
    path('', add_post, name='index'),
    # Дополнительные URL-шаблоны для других страниц
]