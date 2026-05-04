from rest_framework import serializers

from apps.posts.models import Post, PostAttachment
from apps.users.models import User
from apps.users.serializers import GetUserSerializer


class GetPostSerializer(serializers.ModelSerializer):
    attachments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = "__all__"

    def get_attachments(self, obj):
        request = self.context.get("request")
        return [
            request.build_absolute_uri(attachment.file.url)
            if request and attachment.file
            else attachment.file.url
            for attachment in obj.attachments.all()
        ]


class GetPostWithUserSerializer(GetPostSerializer):
    author = GetUserSerializer()


class GetUserPostsSerializer(serializers.ModelSerializer):
    posts = GetPostSerializer(many=True)

    class Meta:
        model = User
        fields = ["username", "email", "img", "posts"]


class CreatePostSerializer(serializers.ModelSerializer):
    attachments = serializers.ListField(
        child=serializers.FileField(),
        write_only=True,
        required=False,
        help_text="List of files to attach to the post",
    )

    class Meta:
        model = Post
        fields = "__all__"
        read_only_fields = ["author"]

    def create(self, validated_data):

        files = validated_data.pop("attachments", [])

        post = Post.objects.create(**validated_data)

        for file in files:
            PostAttachment.objects.create(post=post, file=file)
        return post


class UpdatePostSerializer(serializers.ModelSerializer):
    # TODO: update this serializer to allow attachments update
    class Meta:
        model = Post
        fields = ["title", "content"]
