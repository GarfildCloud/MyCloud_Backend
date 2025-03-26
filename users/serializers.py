import re
from rest_framework import serializers
from .models import CustomUser


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'full_name', 'email', 'password']

    def validate_username(self, value):
        if not re.match(r'^[A-Za-z][A-Za-z0-9]{3,19}$', value):
            raise serializers.ValidationError(
                "Логин должен быть от 4 до 20 символов, начинаться с буквы, содержать только латиницу и цифры"
            )
        return value

    def validate_password(self, value):
        if len(value) < 6 or not re.search(r'[A-Z]', value) or not re.search(r'\d', value) or not re.search(
                r'[!@#$%^&*(),.?":{}|<>]', value):
            raise serializers.ValidationError(
                "Пароль должен содержать минимум 6 символов, включая заглавную букву, цифру и спецсимвол"
            )
        return value

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'full_name', 'email', 'is_admin']
