from rest_framework import serializers

from movieapp.models.actors_models import Actor


class ActorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = "__all__"