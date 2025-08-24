from rest_framework import serializers

from movieapp.models.actors_models import Actor


class ActorsSerializer(serializers.ModelSerializer):
    """
    Serializer for the Actor model.

    This serializer includes all fields of the Actor model (`__all__`) 
    and is mainly used for creating, retrieving, updating, 
    and deleting actor instances (CRUD operations).
    """
    class Meta:
        model = Actor
        fields = "__all__"