from django.shortcuts import render
from django.contrib.auth import get_user_model

# Create your views here.
from rest_framework.generics import ListAPIView, RetrieveDestroyAPIView, CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q

from src.apps.api.serializers import PostSerializer,PostCreateSerializer,CommentSerializer, UserDetaileView, UserSeachView
from src.apps.post.models import Post 
from rest_framework import generics , permissions
from rest_framework.exceptions import ValidationError


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

