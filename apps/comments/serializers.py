from rest_framework import serializers
from apps.users.serializers import GetUserSerializer
from .models import PostComment


class GetPostCommentSerializer(serializers.ModelSerializer):
    author = GetUserSerializer()

    class Meta:
        model = PostComment
        fields = ["id", "author", "content"]


class CreatePostCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostComment
        fields = ["post", "author", "content"]
        read_only_fields = ["post", "author"]
