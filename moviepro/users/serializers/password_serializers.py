from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for changing the user's password.

    Fields:
        old_password (CharField): The user's current password. Required for validation.
        new_password (CharField): The new password the user wants to set. Must pass Django's password validators.
        confirm_password (CharField): Must match the new password to ensure correctness.

    Methods:
        validate_old_password(value):
            Verifies that the provided old password matches the user's current password.
            Raises:
                serializers.ValidationError: If the old password is incorrect.

        save(**kwargs):
            Sets the user's password to the new password after successful validation.
            Saves the user instance and returns it.
    """
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect")
        return value

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user