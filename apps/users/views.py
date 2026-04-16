from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from .serializers import GetUserSerializer, CreateUserSerializer
from .models import User


class UsersAPIView(APIView):
    """
    List all the users or create a new one,
    you need to be an authenticated user to list the users and an Admin user to create a new one
    """

    def get_permissions(self):
        permission_classes = [permissions.IsAdminUser]
        if self.request.method == "GET":
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    def get(self, request):
        users = User.objects.all()
        serializer = GetUserSerializer(instance=users, many=True)
        return Response(serializer.data, status=200)

    def post(self, request):
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                GetUserSerializer(instance=user).data,
                status=status.HTTP_201_CREATED,
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )
