from rest_framework import serializers

from apps.blog.models import Post
from apps.users.models import User
from apps.users.serializers import GetUserSerializer


class GetPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"


class GetPostWithUserSerializer(GetPostSerializer):
    author = GetUserSerializer()


class GetUserPostsSerializer(serializers.ModelSerializer):
    posts = GetPostSerializer(many=True)

    class Meta:
        model = User
        fields = ["username", "email", "posts"]


class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"
        read_only_fields = ["author"]


class UpdatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ["title", "content"]
