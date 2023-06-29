from django.urls import path


from src.apps.account import views

urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/",views.user_logout, name="logout"),
    # path("register/", views.UserRegisterView.as_view(), name="register"),
    path("register/", views.register_user, name="register")
]
