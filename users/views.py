from django.contrib.auth import logout
from django.shortcuts import get_object_or_404
from rest_framework import status, permissions, generics
from rest_framework.decorators import permission_classes, api_view
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from core.logging_utils import log_action
from .models import CustomUser
from .serializers import RegisterSerializer, UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken


class CustomTokenObtainPairView(TokenObtainPairView):
    @log_action("вход в систему (login)")
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class RegisterView(APIView):
    permission_classes = []

    @log_action("регистрация пользователя")
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IsAdmin(permissions.BasePermission):

    @log_action("проверка прав администратора")
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin


class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdmin]


class UserDeleteView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    @log_action("удаление пользователя")
    def delete(self, request, user_id):
        try:
            user = CustomUser.objects.get(pk=user_id)
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except CustomUser.DoesNotExist:
            return Response({"detail": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    @log_action("logout")
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Выход выполнен, токен заблокирован"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": "Ошибка при выходе: " + str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ToggleAdminView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    @log_action("изменение роли (is_admin)")
    def patch(self, request, user_id):
        try:
            user = CustomUser.objects.get(pk=user_id)
            if user == request.user:
                return Response({"detail": "Нельзя изменить самого себя"}, status=status.HTTP_400_BAD_REQUEST)

            user.is_admin = not user.is_admin
            user.save()
            return Response({
                "id": user.id,
                "username": user.username,
                "is_admin": user.is_admin,
            }, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"detail": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND)

class UserMeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class UserDetailView(APIView):
    permission_classes = [IsAdminUser]

    @log_action("получение данных о пользователе")
    def get(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    @log_action("удаление пользователя")
    def delete(self, request, pk):
        user = get_object_or_404(CustomUser, pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

