from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate

from users.models.user_models import CustomUser


class CustomUserRegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for registering a new CustomUser.

    Validates:
    - Password and password confirmation match.
    - Password conforms to Django's password validation rules.

    Fields:
    - username, email, password, password_two, first_name, last_name, bio, image
    """
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_two = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password", "password_two", "first_name", "last_name", "bio", "image")

    def validate(self, data):
        if data["password"] != data["password_two"]:
            raise serializers.ValidationError("Passwords must match")
        return data

    def create(self, validated_data):
        validated_data.pop("password_two")
        return CustomUser.objects.create_user(**validated_data)

    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data["username"], password=data["password"])
        if user:
            return {"user": user}
        raise serializers.ValidationError("Invalid username or password")

