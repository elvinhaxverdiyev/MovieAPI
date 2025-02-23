from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_object_or_404
from movieapp.models import *
from movieapp.serializers import *
# Create your views here.

class MovieListPostAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MovieSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class MovieDetailAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, id):
        movie = get_object_or_404(Movie, pk=id)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)

    def put(self, request, id):
        movie = get_object_or_404(Movie, pk=id)
        serializer = MovieSerializer(movie, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        movie = get_object_or_404(Movie, pk=id)
        movie.delete()
        return Response({"message": "Movie deleted"}, status=status.HTTP_204_NO_CONTENT)
    
    
class MovieLikeAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get(self, request, id):
        movie = get_object_or_404(Movie, pk=id)
        is_liked = movie.likes.filter(id=request.user.id).exists() 
        return Response({"liked": is_liked}, status=status.HTTP_200_OK)

    def post(self, request, id):
        movie = get_object_or_404(Movie, pk=id)
        movie.likes.add(request.user)
        return Response({"message": "Movie liked"}, status=status.HTTP_200_OK)
    

class MovieUnlikeAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get(self, request, id):  
        movie = get_object_or_404(Movie, pk=id)
        is_unlike = not movie.likes.filter(pk=request.user.id).exists() 
        return Response({"unliked": is_unlike}, status=status.HTTP_200_OK)

    def post(self, request, id):
        movie = get_object_or_404(Movie, pk=id)
        if movie.likes.filter(pk=request.user.id).exists():
            movie.likes.remove(request.user)
            return Response({"message": "Like removed"}, status=status.HTTP_200_OK)
        return Response({"message": "You have not liked this movie"}, status=status.HTTP_400_BAD_REQUEST)

class AddCommentAPIView(APIView):
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
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def delete(self, request, id):
        comment = get_object_or_404(Comment, pk=id)
        if request.user == comment.user:
            comment.delete()
            return Response({"message": "Comment deleted"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)
  

class MovieSearchAPIView(APIView):
    def get(self, request):
        query = request.GET.get("q", "")
        if query:
            movies = Movie.objects.filter(title__icontains=query)  
            movie_data = [{"id": movie.id, "title": movie.title} for movie in movies]
            return Response(movie_data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "No query parameter provided"}, status=status.HTTP_400_BAD_REQUEST)
