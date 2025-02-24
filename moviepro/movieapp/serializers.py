from .models import *
from rest_framework import serializers

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    
    class Meta:
        model = Comment
        fields = "__all__"
        
        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class MovieSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Movie
        fields = "__all__"

    def get_likes_count(self, obj):
        return obj.likes.count()  


class MovieCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ["title", "description", "genres", "actors", "trailer_link"]  
        extra_kwargs = {
            "genres": {"required": True},  
        }

    def create(self, validated_data):
        genres = validated_data.pop("genres", [])  
        movie = Movie.objects.create(**validated_data) 

        movie.genres.set(genres)  
        return movie
    
    
class MovieUpdateSerializer(serializers.ModelSerializer):
    likes_count = serializers.IntegerField(read_only=True) 

    class Meta:
        model = Movie
        fields = ["title", "description", "actors", "trailer_link", "genres", "views_count", "likes_count"]

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get("description", instance.description)
        instance.actors = validated_data.get("actors", instance.actors)
        instance.trailer_link = validated_data.get("trailer_link", instance.trailer_link)
        
        genres = validated_data.get("genres")
        if genres is not None:
            instance.genres.set(genres)  
        
        instance.views_count = validated_data.get("views_count", instance.views_count)
        instance.save()
        return instance