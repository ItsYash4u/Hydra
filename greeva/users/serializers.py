from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserDTO(serializers.ModelSerializer):
    """
    DTO for User Response.
    Excludes sensitive data like password, is_staff, is_superuser unless strictly required for admin.
    """
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'user_type', 'phone_number', 'age', 'station_name']
        read_only_fields = ['id', 'email', 'user_type']

class UserUpdateDTO(serializers.ModelSerializer):
    """
    DTO for User Update.
    Allows updating profile fields.
    """
    class Meta:
        model = User
        fields = ['name', 'phone_number', 'age', 'station_name']

class AuthResponseDTO(serializers.Serializer):
    """
    DTO for Authentication Response.
    """
    message = serializers.CharField()
    token = serializers.CharField(required=False) # If we were using tokens
    user = UserDTO(required=False)
    redirect_url = serializers.CharField(required=False)
