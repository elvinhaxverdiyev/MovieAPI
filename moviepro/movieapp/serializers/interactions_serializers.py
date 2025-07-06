from rest_framework import serializers

from movieapp.models.interactions_models import Comment, MovieLike


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    
    class Meta:
        model = Comment
        fields = "__all__"
        
    
class MovieLikeSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.username", read_only=True) 
    class Meta:
        model = MovieLike
        fields = ["user_name"] 
        

