import hashlib
import uuid
import os
from django.db import models
from django.conf import settings


def user_directory_path(instance, filename):
    # Сохраняем в: media/user_<id>/<unique_id>.ext
    ext = filename.split('.')[-1]
    new_filename = f"{uuid.uuid4().hex}.{ext}"
    return os.path.join(f"user_{instance.owner.id}", new_filename)


class File(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='files')
    original_name = models.CharField(max_length=255)
    stored_file = models.FileField(upload_to=user_directory_path)
    size = models.BigIntegerField()
    upload_date = models.DateTimeField(auto_now_add=True)
    last_download = models.DateTimeField(null=True, blank=True)
    comment = models.TextField(blank=True)
    special_link = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    file_hash = models.CharField(max_length=64, editable=False, default=None)

    def save(self, *args, **kwargs):
        if not self.file_hash and self.stored_file:
            # вычисляем SHA256-хеш файла
            hasher = hashlib.sha256()
            for chunk in self.stored_file.chunks():
                hasher.update(chunk)
            self.file_hash = hasher.hexdigest()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.original_name
