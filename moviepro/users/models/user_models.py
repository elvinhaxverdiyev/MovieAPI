from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Custom user model that extends Django's built-in AbstractUser.

    Additional Fields:
    - email (EmailField): Unique email address. Can be null or blank.
    - bio (TextField): A short biography or description of the user (max 550 characters).
    - image (ImageField): Optional profile image uploaded to 'images/' directory.

    Inherits all fields and functionality from AbstractUser (e.g., username, password, etc.).
    """
    email = models.EmailField(unique=True, null=True, blank=True)
    bio = models.TextField(max_length=550, null=True, blank=True)
    image = models.ImageField(upload_to="images/", null=True, blank=True)

    def __str__(self):
        return f"{self.username}"