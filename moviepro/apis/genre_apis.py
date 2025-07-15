from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.core.cache import cache
import logging

from movieapp.models import Category
from movieapp.serializers import CategorySerializer
from movieapp.models import Movie
from movieapp.serializers import MovieSerializer

__all__ = [
    "GenreListAPIView",
    "MovieByGenreAPIView"
]

logger = logging.getLogger(__name__)

class GenreListAPIView(APIView):
    def get(self, request):
        categories = cache.get('categories')
        logger.info(f"Cachedən categories: {categories}")

        if not categories:
            categories_qs = Category.objects.all()
            serializer = CategorySerializer(categories_qs, many=True)
            categories = serializer.data
            cache.set('categories', categories, timeout=31536000)
            logger.info("Cache yeniləndi")
        else:
            logger.info("Cache istifadə edildi")

        return Response(categories, status=status.HTTP_200_OK)
    
            
class MovieByGenreAPIView(APIView):
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
                return Response({"error": "Genre not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"error": "Genre parameter is required"}, status=status.HTTP_400_BAD_REQUEST)