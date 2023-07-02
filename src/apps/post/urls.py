from django.urls import path

from src.apps.post import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path("add_post/", views.add_post, name="add_post")
]