from django.contrib.auth import login, logout
from django.shortcuts import get_object_or_404
from rest_framework import status, permissions, generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from core.logging_utils import log_action
from .models import CustomUser
from .serializers import RegisterSerializer, UserSerializer

from django.contrib.auth import logout
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_GET


class RegisterView(APIView):
    permission_classes = []
    authentication_classes = []

    @log_action("регистрация пользователя")
    def post(self, request):
        print(request.data)
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            login(request, user)
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = []

    @log_action("вход в систему")
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response(
                {"detail": "Необходимо указать username и password"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = CustomUser.objects.filter(username=username).first()
        if user and user.check_password(password):
            login(request, user)
            return Response(UserSerializer(user).data)
        
        return Response(
            {"detail": "Неверные учетные данные"},
            status=status.HTTP_401_UNAUTHORIZED
        )

@require_GET
def custom_logout(request):
    logout(request)  # Завершает сессию
    return JsonResponse({"detail": "Successfully logged out."}, status=200)


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
        # Удаляем пользователя
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

