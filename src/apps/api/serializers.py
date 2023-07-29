from rest_framework import serializers


from src.apps.post.models import Post
from src.apps.account.models import User

class PostSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Post
        fields = "__all__"


class PostCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Post
        fields = ["description", "image"]

class UserDetaileView(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = "__all__"

class UserSeachView(serializers.ModelSerializer):

        class Meta:
            model = User
            fields = "__all__"