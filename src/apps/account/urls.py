from django.urls import path



from src.apps.account import views
from .views import UsersSearchListView


urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/",views.user_logout, name="logout"),
    path('unfollow/<int:pk>/', views.unfollow, name='unfollow'),
    path('follow/<int:pk>/', views.follow, name='follow'),
    
]

