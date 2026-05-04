from rest_framework.generics import ListCreateAPIView
from .models import PostComment
from .serializers import GetPostCommentSerializer, CreatePostCommentSerializer


class PostCommentsList(ListCreateAPIView):
    lookup_url_kwarg = "post_id"

    def get_queryset(self):
        post_id = self.kwargs.get("post_id")
        return PostComment.objects.filter(post__id=post_id).order_by("-created_at")

    def perform_create(self, serializer):
        post_id = self.kwargs.get("post_id")
        serializer.save(post_id=post_id, author=self.request.user)

    def get_serializer_class(self):
        if self.request.method == "GET":
            return GetPostCommentSerializer
        return CreatePostCommentSerializer
