from rest_framework.views import APIView, Response
from .models import Post
from .serializers import (
    GetPostSerializer,
    GetPostWithUserSerializer,
    GetUserPostsSerializer,
    CreatePostSerializer,
)
from rest_framework import status, permissions
from apps.users.models import User


class PostListView(APIView):
    # TODO: pagination

    permission_classes = [permissions.IsAuthenticated]

    # TODO: Get posts for connections only
    def get(self, request):
        posts = Post.objects.order_by("-created_at").all()
        serializer = GetPostWithUserSerializer(instance=posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CreatePostSerializer(
            data={**request.data, "author": request.user.id}
        )
        if serializer.is_valid():
            post = serializer.save()
            return Response(
                GetPostSerializer(instance=post).data, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserPostsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = User.objects.prefetch_related().get(pk=request.user.id)
        serializer = GetUserPostsSerializer(instance=user)
        return Response(serializer.data)
