from django.urls import path
from apps.users import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path("", views.UsersAPIView.as_view(), name="users_list"),
    path("login/", TokenObtainPairView.as_view(), name="user_login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="user_token_refresh"),
]
