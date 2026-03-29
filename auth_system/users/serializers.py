from rest_framework import serializers
from .models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'password_confirm', 'first_name', 'last_name', 'middle_name']

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError("Passwords do not match")
        if len(data['password']) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters")
        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

class UserResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'middle_name', 'created_at']


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для обновления профиля пользователя.
    Не включает email, так как email обычно нельзя менять или это требует подтверждения.
    """

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'middle_name']

    def validate_first_name(self, value):
        """Валидация имени"""
        if value and len(value) < 2:
            raise serializers.ValidationError("First name must be at least 2 characters")
        if value and len(value) > 50:
            raise serializers.ValidationError("First name must be less than 50 characters")
        return value

    def validate_last_name(self, value):
        """Валидация фамилии"""
        if value and len(value) < 2:
            raise serializers.ValidationError("Last name must be at least 2 characters")
        if value and len(value) > 50:
            raise serializers.ValidationError("Last name must be less than 50 characters")
        return value

    def validate_middle_name(self, value):
        """Валидация отчества (опционально)"""
        if value and len(value) > 50:
            raise serializers.ValidationError("Middle name must be less than 50 characters")
        return value