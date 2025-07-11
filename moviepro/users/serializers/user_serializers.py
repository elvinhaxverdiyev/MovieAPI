from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate

from users.models.user_models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer for the CustomUser model.

    This serializer handles the serialization and deserialization of user data,
    including fields such as username, email, first and last name, bio, and profile image.

    Fields:
        - id: The unique identifier of the user.
        - username: The user's username.
        - email: The user's email address (optional).
        - first_name: The user's first name.
        - last_name: The user's last name.
        - bio: A short biography or description for the user (optional).
        - image: The user's profile image (optional).

    Note:
        The email, bio, and image fields are optional and can be left blank.
    """
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