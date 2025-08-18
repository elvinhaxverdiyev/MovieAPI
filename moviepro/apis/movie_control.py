from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.authentication import TokenAuthentication

from .pagginations import MoviePagination
from users.serializers import *
from movieapp.models import *
from movieapp.serializers import *
from users.models import *
from notifications.sendmail import send_movie_created_email

__all__ = [
    "MovieListPostAPIView",
    "MovieDetailAPIView",
]


class MovieListPostAPIView(APIView):
    """API that retrieves a list of movies and allows adding new ones."""
    
    permission_classes = [AllowAny]  
    pagination_class = MoviePagination
    http_method_names = ['get', 'post']
    
    def get(self, request):
        movies = Movie.objects.all()  
        pagination = self.pagination_class()  
        result_page = pagination.paginate_queryset(movies, request) 
        serializer = MovieSerializer(result_page, many=True)  
        return pagination.get_paginated_response(serializer.data) 
    
    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(
                {"detail": "You must be logged in to create a movie."}, 
                status=status.HTTP_401_UNAUTHORIZED
                )
        
        permission_classes = [IsAuthenticated]  
        
        serializer = MovieCreateSerializer(data=request.data)

        if serializer.is_valid():
            movie = serializer.save(created_by=request.user) 
            send_movie_created_email(movie)  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class MovieDetailAPIView(APIView):
    authentication_classes = [TokenAuthentication]  
    http_method_names = ['get', 'patch', 'delete']
    
    def get_permissions(self):
        if self.request.method == "GET":
            return [AllowAny()]
        return [IsAuthenticated()]
    
    def get(self, request, id):
        try:
            movie = Movie.objects.get(pk=id) 
            serializer = MovieSerializer(movie)
            return Response(serializer.data)
        except Movie.DoesNotExist:
            return Response({"detail": "Movie not found."}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, id):
        movie = get_object_or_404(Movie, pk=id)
        if request.user != movie.created_by:
            return Response({"error": "You do not have permission to edit this movie"},
                            status=status.HTTP_403_FORBIDDEN)
        
        serializer = MovieUpdateSerializer(movie, data=request.data, partial=True)
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
        return Response({"message": "Movie deleted"}, 
                        status=status.HTTP_204_NO_CONTENT
                        )