from django.urls import path

from src.apps.post import views

urlpatterns = [
    path('', views.IndexPageView.as_view( ), name="index"),
]