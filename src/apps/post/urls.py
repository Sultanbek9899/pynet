from django.urls import path

from src.apps.post import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path("add_post/", views.add_post, name="add_post"),
    path('<uuid:post_id>like', views.like_post,name='post_like'),
    path('add_comment/', views.create_comment, name='create_comment')
]