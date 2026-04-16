from django.urls import path
from .views import PostListView, UserPostsView

urlpatterns = [
    path("posts/", PostListView.as_view(), name="posts_list"),
    path("posts/u/", UserPostsView.as_view(), name="user_posts"),
]
