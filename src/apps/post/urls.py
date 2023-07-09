from django.urls import path

from src.apps.post import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path("add_post/", views.add_post, name="add_post"),
    path('recommendations/', views.recommendations_view, name='recommendations'),
    path('post_details/<int:pk>/', views.post_details, name='post_details'),
    path('like_post/<int:post_id>/', views.like_post, name='like_post'),
    path('like_comment/<int:comment_id>/', views.like_comment, name='like_comment'),
]