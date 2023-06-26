from django.urls import path

from src.apps.post import views 
from .views import get_feed 

urlpatterns = [
    path('',  views.IndexPageView.as_view(), name="index"),
    path('index.html/', get_feed, name="index.html"),
]