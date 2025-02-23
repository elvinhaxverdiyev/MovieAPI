from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination

from movieapp.models import *
from movieapp.serializers import *

# Create your views here.

class MovieByGenreAPIView(APIView):
    """API that lists movies based on the specified genre."""
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

        

class MoviePagination(PageNumberPagination):
    """Pagination class that splits the movie list into pages."""
    page_size = 2
    

class MovieListPostAPIView(APIView):
    """API that retrieves a list of movies and allows adding new ones."""
    pagination_class = MoviePagination

    def get(self, request):
        movies = Movie.objects.all()

        pagination = self.pagination_class()  
        result_page = pagination.paginate_queryset(movies, request) 

        serializer = MovieSerializer(result_page, many=True)  
        return pagination.get_paginated_response(serializer.data) 

    def post(self, request, *args, **kwargs):
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class MovieDetailAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, id):
        movie = get_object_or_404(Movie, pk=id)
        movie.views_count += 1
        movie.save(update_fields=["views_count"])
        like_count = MovieLike.objects.filter(movie=movie).count()
        
        serializer = MovieSerializer(movie)
        return Response({
            "movie": serializer.data,
            "like_count": like_count,
            "views_count": movie.views_count,
        }, status=status.HTTP_200_OK)

    def put(self, request, id):
        movie = get_object_or_404(Movie, pk=id)

        if request.user != movie.created_by:
            return Response({"error": "You do not have permission to edit this movie"}, 
                            status=status.HTTP_403_FORBIDDEN)

        serializer = MovieSerializer(movie, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        movie = get_object_or_404(Movie, pk=id)

        if request.user != movie.created_by: 
            return Response({"error": "You do not have permission to delete this movie"}, 
                            status=status.HTTP_403_FORBIDDEN
                            )

        movie.delete()
        return Response({"message": "Movie deleted"}, status=status.HTTP_204_NO_CONTENT
                        )

    
    
class MovieLikeAPIView(APIView):
    """API that handles liking a movie."""
    
    def post(self, request, id):
        movie = get_object_or_404(Movie, pk=id)

        if MovieLike.objects.filter(user=request.user, movie=movie).exists():
            return Response({"message": "You have already liked this movie"}, status=status.HTTP_400_BAD_REQUEST)

        MovieLike.objects.create(user=request.user, movie=movie)
        return Response({"message": "Movie liked"}, status=status.HTTP_201_CREATED)
    

class MovieUnlikeAPIView(APIView):
    """API that removes a like from a previously liked movie."""
    
    def post(self, request, id):
        movie = get_object_or_404(Movie, pk=id)

        like = MovieLike.objects.filter(user=request.user, movie=movie).first()
        if not like:
            return Response({"message": "You have not liked this movie"}, status=status.HTTP_400_BAD_REQUEST)

        like.delete()
        return Response({"message": "Like removed"}, status=status.HTTP_200_OK)


class AddCommentAPIView(APIView):
    """API that allows adding comments to a movie and viewing existing comments."""
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get(self, request, id):
        movie = get_object_or_404(Movie, pk=id)
        comments = Comment.objects.filter(movie=movie)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, id):
        movie = get_object_or_404(Movie, pk=id)
        comment = Comment.objects.create(
            movie=movie,
            user=request.user,
            text=request.data.get("text")
        )
        return Response(CommentSerializer(comment).data, status=status.HTTP_201_CREATED)
    

class DeleteCommentAPIView(APIView):
    """API that allows users to delete their own comments."""
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def delete(self, request, id):
        comment = get_object_or_404(Comment, pk=id)
        if request.user == comment.user:
            comment.delete()
            return Response({"message": "Comment deleted"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)
  

class MovieSearchAPIView(APIView):
    """API that searches for movies by title."""
    def get(self, request):
        query = request.GET.get("q", "")
        if query:
            movies = Movie.objects.filter(title__icontains=query)  
            movie_data = [{"id": movie.id, "title": movie.title} for movie in movies]
            return Response(movie_data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "No query parameter provided"}, status=status.HTTP_400_BAD_REQUEST)
