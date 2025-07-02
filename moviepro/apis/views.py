from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from users.serializers import *
from movieapp.models import *
from movieapp.serializers import *
from users.models import *

    
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
    
