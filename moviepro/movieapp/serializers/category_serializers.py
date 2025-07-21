from rest_framework import serializers

from movieapp.models.category_models import Category

        
class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer class for the Category model.

    This serializer automatically includes all fields of the Category model
    and is typically used for converting model instances to and from JSON
    for API interactions.

    Usage:
        - Serialize Category instances to JSON.
        - Deserialize JSON data to create/update Category instances.
    """
    class Meta:
        model = Category
        fields = "__all__"