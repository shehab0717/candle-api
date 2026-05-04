from django.urls import path
from .views import PostCommentsList

urlpatterns = [
    path("post/<int:post_id>/", PostCommentsList.as_view(), name="post_comments")
]
