from django.urls import path

from src.apps.post import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path("add_post/", views.add_post, name="add_post"),
    path('add_to_bookmarks/<int:post_id>/', views.add_to_bookmarks, name='add_to_bookmarks'),
    path('remove_from_bookmarks/<int:post_id>/', views.remove_from_bookmarks, name='remove_from_bookmarks'),
    path('bookmarks/', views.get_bookmarks, name='bookmarks'),
]