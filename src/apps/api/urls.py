from django.urls import path

from src.apps.api import views

from .views import CommentCreateAPIView , UserPostListView, EditProfile, FollowApiView, UnfollowApiView



from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)   
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(
    openapi.Info(
        title="PyNET.KG Api",
        default_version='v1',
        description="PyNET.KG Api",
        contact=openapi.Contact(email="sultanbek9899@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
)


urlpatterns = [
    path('docs/', schema_view.with_ui("swagger")),
    path('post/list/', views.PostListAPIView.as_view()),
    path('post/<int:pk>/', views.PostDetailAPIView.as_view()),
    path('post/like/delete/<int:pk>', views.DeleteLikeAPIView.as_view()),
    path('post/create/', views.PostCreateAPIView.as_view()),
    path("some/api/", views.SomeApi.as_view()),
    path('edit/profile/<int:pk>/', views.EditProfile.as_view(), name='edit_profile'),
    path('users/<int:pk>/', views.UserDetailsView.as_view()),
    path('users/search/', views.UserSearchView.as_view()),
    path('user/follow/<int:pk>/', views.FollowApiView.as_view()),
    path('user/unfollow/<int:pk>/', views.UnfollowApiView.as_view()),
    
    #authentication
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('create-comment/', CommentCreateAPIView.as_view(), name='comment-create'),
    path('user_posts/', UserPostListView.as_view(), name='user-posts-list'),
]