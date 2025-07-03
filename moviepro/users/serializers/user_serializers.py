from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate

from users.models.user_models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "image",
        )
        extra_kwargs = {
            "email": {"required": False, "allow_blank": True},
            "bio": {"required": False, "allow_blank": True},
            "image": {"required": False},
        }