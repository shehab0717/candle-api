from django.urls import path
from .views import UserPostsView
from . import views

urlpatterns = [
    path("", views.PostList.as_view(), name="posts_list"),
    path("u/", UserPostsView.as_view(), name="user_posts"),
    path("<int:post_id>/", views.PostView2.as_view(), name="post_detail"),
]
