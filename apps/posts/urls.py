from django.urls import path
from .views import UserPostsView
from . import views

urlpatterns = [
    path("posts/", views.PostList.as_view(), name="posts_list"),
    path("posts/u/", UserPostsView.as_view(), name="user_posts"),
    path("posts/<int:post_id>/", views.PostView2.as_view(), name="post_detail"),
]
