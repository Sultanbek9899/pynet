from django.urls import path



from src.apps.account import views
from .views import UsersSearchListView


urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/",views.user_logout, name="logout"),
    
  
    path("register/", views.register_user, name="register"),
    
    path('profile/<int:pk>/', views.get_user_profile, name="profile" ),
    path('edit/profile/', views.UserUpdateProfile.as_view(), name="edit_profile"),
  
    path('unfollow/<int:pk>/', views.unfollow, name='unfollow'),
    path('follow/<int:pk>/', views.follow, name='follow'),
    
]

