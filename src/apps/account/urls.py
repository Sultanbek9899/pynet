from django.urls import path



from src.apps.account import views
from account.views import UsersSearchListView


urlpatterns = [
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/",views.user_logout, name="logout"),
    # path('search/', UsersSearchListView(), name='user_search')
    path('follow', views.follow, name='follow')
]

