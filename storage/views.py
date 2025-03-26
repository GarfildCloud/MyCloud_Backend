import logging
import uuid

from django.http import Http404, FileResponse
from django.utils import timezone
from django.utils.encoding import smart_str
from rest_framework import generics, permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView

from core.logging_utils import log_action
from .models import File
from .serializers import FileSerializer, FileUpdateSerializer

logger = logging.getLogger(__name__)


class FileListCreateView(generics.ListCreateAPIView):
    serializer_class = FileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        requested_user_id = self.request.query_params.get("user_id")

        # Если админ — может запрашивать чужие файлы
        if user.is_admin and requested_user_id:
            return File.objects.filter(owner__id=requested_user_id)
        return File.objects.filter(owner=user)

    @log_action("загрузка файла")
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class FileDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = File.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return FileSerializer
        return FileUpdateSerializer

    def get_object(self):
        file = super().get_object()
        user = self.request.user
        if file.owner != user and not user.is_admin:
            raise PermissionDenied("У вас нет доступа к этому файлу.")
        return file


class FileDownloadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        try:
            file = File.objects.get(pk=pk)
        except File.DoesNotExist:
            raise Http404("Файл не найден")

        user = request.user
        if file.owner != user and not user.is_admin:
            raise PermissionDenied("У вас нет доступа к этому файлу.")

        file.last_download = timezone.now()
        file.save(update_fields=["last_download"])

        response = FileResponse(file.stored_file.open("rb"), as_attachment=True)
        response["Content-Disposition"] = f'attachment; filename="{smart_str(file.original_name)}"'
        return response


class FilePublicDownloadView(APIView):
    permission_classes = []  # доступ для всех

    def get(self, request, link_uuid):
        try:
            file = File.objects.get(special_link=link_uuid)
        except File.DoesNotExist:
            raise Http404("Файл не найден")

        file.last_download = timezone.now()
        file.save(update_fields=["last_download"])

        response = FileResponse(file.stored_file.open("rb"), as_attachment=True)
        response["Content-Disposition"] = f'attachment; filename="{smart_str(file.original_name)}"'
        return response


class RegenerateLinkView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @log_action("перегенерация ссылки на скачивание")
    def patch(self, request, pk):
        try:
            file = File.objects.get(pk=pk)
        except File.DoesNotExist:
            return Response({"detail": "Файл не найден"}, status=status.HTTP_404_NOT_FOUND)

        if file.owner != request.user and not request.user.is_admin:
            raise PermissionDenied("Нет доступа к файлу")

        file.special_link = uuid.uuid4()
        file.save(update_fields=["special_link"])

        return Response({
            "id": file.id,
            "special_link": str(file.special_link)
        }, status=status.HTTP_200_OK)
