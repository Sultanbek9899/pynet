from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib import messages
# Create your views here.
from rest_framework.generics import ListAPIView, RetrieveDestroyAPIView, CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from src.apps.api.serializers import PostSerializer,PostCreateSerializer,CommentSerializer, UserDetaileView, UserSeachView, FollowUnfollowSerializer
from src.apps.post.models import Post 
from rest_framework import generics , permissions
from rest_framework.exceptions import ValidationError
from rest_framework import status
from .serializers import UserUpdateSerializer 
from ..account.models import User
from src.apps.account.models import User



class PostListAPIView(ListAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]


class PostDetailAPIView(RetrieveDestroyAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    

class PostCreateAPIView(CreateAPIView):
    serializer_class = PostCreateSerializer
    permission_classes = [IsAuthenticated]


    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    
class SomeApi(APIView):
    permission_classes = []

    def get(self,request):
        data = {"status":"Ok", "info":"your post is reposted"}
        return Response(data=data, status=200)
    
class CommentCreateAPIView(CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        post_id = self.request.data.get('post_id')

        if post_id:
            try:
                post = Post.objects.get(pk=post_id)
                serializer.save(post=post)
            except Post.DoesNotExist:
                serializer.errors['post_id'] = ['Post with the given post_id does not exist.']
                raise ValidationError(serializer.errors)
            

class UserPostListView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Получаем посты только текущего аутентифицированного пользователя
        return Post.objects.filter(author=self.request.user)



class EditProfile(RetrieveUpdateAPIView):
    serializer_class = UserUpdateSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated] 

    
class UserDetailsView(APIView):
    def get(self,request, pk):
        user = User.objects.get(pk=pk)
        serializer = UserDetaileView(user)
        return Response(data=serializer.data,status=200)
    
    

class UserSearchView(APIView):
    def get(self, request):
        query = self.request.query_params.get('query')
        users = User.objects.all() 
        if query: 
            users = users.filter(Q(username__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query))

        serializer = UserSeachView(users, many=True)
        return Response(serializer.data)



class FollowApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, pk):
        try:
            follow_user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
       
        if request.user != follow_user:
            if request.user not in follow_user.followers.all():
                follow_user.followers.add(request.user)
                # return messages.success(request, f'Вы подписались на {follow_user.username}')
                return Response({"details":f"Вы подписались на {follow_user.username}"}, status=status.HTTP_201_CREATED)
            else:
                # return messages.info(request, f'Вы уже подписаны на {follow_user.username}')
                return Response({"detals": f"Вы уже подписаны на {follow_user.username}"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # return messages.info(request, 'Вы не можете подписаться на самого себя')
            return Response({"details": "Вы не можете подписаться на самого себя"}, status=status.HTTP_400_BAD_REQUEST)

        # serializer = FollowUnfollowSerializer(follow_user)
        # return Response(serializer.data)
    
    def get(self, request, pk):
        user = User.objects.get(pk=pk)
        followers = user.followers.all()
        follower_serializer = UserDetaileView(instance=followers, many=True)
        return Response(follower_serializer.data)


class UnfollowApiView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, pk):
        try:
            unfollow_user= User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
      
        if request.user != unfollow_user:
            if request.user in unfollow_user.followers.all():
                unfollow_user.followers.remove(request.user)
                # return messages.success(request, f'Вы отписались от {unfollow_user.username}')
                return Response({"details":f"Вы отписались от {unfollow_user.username}"}, status=status.HTTP_200_OK)
            else:
                # return messages.info(request, f'Вы не были подписаны на {unfollow_user.username}')
                return Response({"details":f"Вы не были подписаны на {unfollow_user.username}"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            # return messages.info(request, 'Вы не можете отписаться от самого себя')
            return Response({"details":"Вы не можете отписаться от самого себя"}, status=status.HTTP_400_BAD_REQUEST)

        # serializer = FollowUnfollowSerializer(unfollow_user)
        # return Response(serializer.data)
    
    def get(self,request, pk):
        user = User.objects.get(pk=pk)
        followings = user.followers.all()
        followings_serializer = UserDetaileView(followings, many=True)
        return Response(followings_serializer.data)