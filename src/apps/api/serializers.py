from rest_framework import serializers
from django.contrib.auth import get_user_model
from src.apps.post.models import Post

from ..account.models import User

class PostSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Post
        fields = "__all__"


class PostCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Post
        fields = ["description", "image"]


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "birthday", "email", "mobile", "about", "avatar", "is_private", "gender" ]