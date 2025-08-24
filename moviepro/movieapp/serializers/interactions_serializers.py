from rest_framework import serializers

from movieapp.models.interactions_models import Comment, MovieLike


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Comment model.

    This serializer converts Comment instances to and from JSON format.
    It includes all fields from the Comment model, but represents the
    related user using its `__str__` method via StringRelatedField.
    """
    user = serializers.StringRelatedField()
    
    class Meta:
        model = Comment
        fields = "__all__"
        
    
class MovieLikeSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.username", read_only=True) 
    class Meta:
        model = MovieLike
        fields = ["user_name"] 
        

