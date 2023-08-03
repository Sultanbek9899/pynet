
from rest_framework import serializers
from django.contrib.auth import get_user_model
from src.apps.post.models import Post, Comment
from src.apps.account.models import User

from ..account.models import User

class PostSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Post
        fields = "__all__"


class PostCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Post
        fields = ["description", "image"]   

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "birthday", "email", "mobile", "about", "avatar", "is_private", "gender" ]

class UserDetaileView(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"

class UserSeachView(serializers.ModelSerializer):

        class Meta:
            model = User
            fields = "__all__"


class LikeCreateSerializer(serializers.Serializer):
    post_id = serializers.IntegerField()

    def validate(self, attrs):
        id_ = attrs.get("post_id")
        try:
            Post.objects.get(pk=id_)
        except Post.DoesNotExist:
            raise serializers.ValidationError({"error": "post does not exist"})
        else:
            return attrs




