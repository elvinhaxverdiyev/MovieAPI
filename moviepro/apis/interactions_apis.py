from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.authentication import TokenAuthentication

from .permission_class import HeHasPermission
from users.serializers import *
from movieapp.models import *
from movieapp.serializers import *
from users.models import *

__all__ = [
    "MovieLikeAPIView",
    "AddCommentAPIView",
    "DeleteCommentAPIView"
]


class MovieLikeAPIView(APIView):
    """API that handles liking a movie."""
    permission_classes = [IsAuthenticatedOrReadOnly]
    http_method_names = ['get', 'post']
    
    def get(self, request, id):
        movie = get_object_or_404(Movie, pk=id)
        likes_count = MovieLike.objects.filter(movie=movie).count()
        likes = MovieLike.objects.filter(movie=movie).values("user__id") 
        return Response({
            "movie": movie.title,
            "likes_count": likes_count,
            "likes": list(likes)  
        }, status=status.HTTP_200_OK)

    def post(self, request, id):
        movie = get_object_or_404(Movie, pk=id)
        user = request.user if request.user.is_authenticated else None

        if MovieLike.objects.filter(user=user, movie=movie).exists():
            return Response({"message": "You have already liked this movie"},
                            status=status.HTTP_400_BAD_REQUEST
                            )

        MovieLike.objects.create(user=user, movie=movie)
        movie.likes_count = movie.likes.count() 
        movie.save()
        return Response({"message": "Movie liked"}, 
                        status=status.HTTP_201_CREATED
                        )


class AddCommentAPIView(APIView):
    """API that allows adding comments to a movie and viewing existing comments."""

    authentication_classes = [TokenAuthentication]
    permission_classes = [HeHasPermission]
    http_method_names = ['get', 'post']
        
    def get(self, request, id):
        movie = get_object_or_404(Movie, pk=id)
        comments = Comment.objects.filter(movie=movie)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, id):
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials were not provided."}, status=status.HTTP_401_UNAUTHORIZED)

        movie = get_object_or_404(Movie, pk=id)
        comment = Comment.objects.create(
            movie=movie,
            user=request.user,
            text=request.data.get("text")
        )
        return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)


class DeleteCommentAPIView(APIView):
    """API that allows users to delete their own comments."""
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, HeHasPermission]
    http_method_names = ['delete']
        
    def delete(self, request, id):
        comment = get_object_or_404(Comment, pk=id)
        if request.user == comment.user:
            comment.delete()
            return Response({"message": "Comment deleted"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)