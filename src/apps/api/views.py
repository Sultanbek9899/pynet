from django.shortcuts import render

# Create your views here.
from rest_framework.generics import ListAPIView, RetrieveDestroyAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from src.apps.api.serializers import PostSerializer,PostCreateSerializer,CommentSerializer
from src.apps.post.models import Post 
from rest_framework import generics , permissions
from rest_framework.exceptions import ValidationError

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