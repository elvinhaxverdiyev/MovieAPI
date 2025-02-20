from .models import *
from rest_framework import serializers

class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    
    class Meta:
        model = Comment
        fields = "__all__"

class MovieSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    likes_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Movie
        fields = "__all__"

    def get_likes_count(self, obj):
        return obj.likes.count()  
