from rest_framework.views import APIView, Response
from .models import Post
from .serializers import (
    GetPostSerializer,
    GetPostWithUserSerializer,
    GetUserPostsSerializer,
    CreatePostSerializer,
    UpdatePostSerializer,
)
from rest_framework import status, permissions
from rest_framework.request import Request
from apps.users.models import User
from django.shortcuts import get_object_or_404
from .permissions import IsBlogAuthor
from rest_framework.generics import RetrieveUpdateDestroyAPIView


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


class PostView(APIView):
    def get_permissions(self):
        perms = [IsBlogAuthor]
        if self.request.method in permissions.SAFE_METHODS:
            perms = [permissions.IsAuthenticated]
        elif self.request.method == "DELETE":
            perms = [IsBlogAuthor | permissions.IsAdminUser]
        return [perm() for perm in perms]

    def get(self, request, post_id):
        post = get_object_or_404(Post.objects.select_related("author"), pk=post_id)
        serializer = GetPostWithUserSerializer(instance=post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, post_id):
        post = get_object_or_404(Post.objects.select_related("author"), pk=post_id)
        self.check_object_permissions(request, post)
        serializer = UpdatePostSerializer(instance=post, data={**request.data})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, post_id):
        post = get_object_or_404(Post.objects.select_related("author"), pk=post_id)
        self.check_object_permissions(request, post)
        post.delete()
        return Response(status=status.HTTP_200_OK)


class PostView2(RetrieveUpdateDestroyAPIView):
    lookup_url_kwarg = "post_id"

    def get_queryset(self):
        return Post.objects.select_related("author")

    def get_serializer_class(self):
        if self.request.method == "GET":
            return GetPostWithUserSerializer
        else:
            return UpdatePostSerializer

    def get_permissions(self):
        perms = [IsBlogAuthor]
        if self.request.method in permissions.SAFE_METHODS:
            perms = [permissions.IsAuthenticated]
        elif self.request.method == "DELETE":
            perms = [IsBlogAuthor | permissions.IsAdminUser]
        return [perm() for perm in perms]
