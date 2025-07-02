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

    
class MovieLikeAPIView(APIView):
    """API that handles liking a movie."""
    permission_classes = [IsAuthenticatedOrReadOnly]
    
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
        
    def delete(self, request, id):
        comment = get_object_or_404(Comment, pk=id)
        if request.user == comment.user:
            comment.delete()
            return Response({"message": "Comment deleted"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)
  

class MovieSearchAPIView(APIView):
    """API that searches for movies by title."""
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get(self, request):
        query = request.GET.get("q", "")
        if query:
            movies = Movie.objects.filter(title__icontains=query)  
            movie_data = [{"id": movie.id, "title": movie.title} for movie in movies]
            return Response(movie_data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "No query parameter provided"}, status=status.HTTP_400_BAD_REQUEST)


class MovieByGenreAPIView(APIView):
    """API that lists movies based on the specified genre."""
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get(self, request):
        genre_name = request.query_params.get("genre", None)

        if genre_name:
            try:
                genre = Category.objects.get(name=genre_name)  
                movies = Movie.objects.filter(genres=genre) 
                serializer = MovieSerializer(movies, many=True) 
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Category.DoesNotExist:
                
                return Response({"error": "Genre not found"}, 
                                status=status.HTTP_404_NOT_FOUND
                                )

        return Response({"error": "Genre parameter is required"},
                        status=status.HTTP_400_BAD_REQUEST
                        )
        

class GenreListAPIView(APIView):
    
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
