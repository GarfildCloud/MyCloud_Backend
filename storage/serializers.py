import hashlib

from django.conf import settings
from django.utils.timezone import localtime
from rest_framework import serializers
from .models import File


class FileSerializer(serializers.ModelSerializer):
    original_name = serializers.ReadOnlyField()
    size = serializers.ReadOnlyField()
    upload_date = serializers.SerializerMethodField()
    last_download = serializers.SerializerMethodField()
    special_link = serializers.ReadOnlyField()
    download_url = serializers.SerializerMethodField()

    class Meta:
        model = File
        fields = [
            'id', 'original_name', 'stored_file', 'size',
            'upload_date', 'last_download', 'comment', 'special_link', 'download_url'
        ]

    def create(self, validated_data):
        uploaded_file = validated_data['stored_file']
        validated_data['original_name'] = uploaded_file.name
        validated_data['size'] = uploaded_file.size
        return super().create(validated_data)

    def validate(self, data):
        user = self.context['request'].user
        uploaded_file = data.get('stored_file')

        # считаем хеш на лету
        hasher = hashlib.sha256()
        for chunk in uploaded_file.chunks():
            hasher.update(chunk)
        file_hash = hasher.hexdigest()

        if File.objects.filter(owner=user, file_hash=file_hash).exists():
            raise serializers.ValidationError("Такой файл уже загружен вами ранее.")

        return data

    def get_download_url(self, obj):
        request = self.context.get('request')
        if request is None:
            return None
        return request.build_absolute_uri(
            f"{settings.API_PREFIX}/storage/public/{obj.special_link}/"
        )


    def format_datetime(self, dt):
        return localtime(dt).strftime("%d.%m.%Y %H:%M") if dt else None

    def get_upload_date(self, obj):
        return self.format_datetime(obj.upload_date)

    def get_last_download(self, obj):
        return self.format_datetime(obj.last_download)


class FileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['original_name', 'comment']
