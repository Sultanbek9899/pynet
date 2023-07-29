from django.shortcuts import render
from django.contrib.auth import get_user_model

# Create your views here.
from rest_framework.generics import ListAPIView, RetrieveDestroyAPIView, CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from src.apps.api.serializers import PostSerializer,PostCreateSerializer
from src.apps.post.models import Post
from .serializers import UserUpdateSerializer 

from ..account.models import User

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
    

class EditProfile(RetrieveUpdateAPIView):
    serializer_class = UserUpdateSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated] 