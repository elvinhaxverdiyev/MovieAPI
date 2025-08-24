from rest_framework import serializers
from movieapp.models import Image

class ImageSerializer(serializers.ModelSerializer):
    """
    Serializer for the Image model.

    This serializer handles the conversion of Image model instances
    to and from JSON. It exposes only the `id` and `image` fields,
    which makes it suitable for lightweight image representation
    in API responses.
    """
    class Meta:
        model = Image
        fields = ("id", "image")  
