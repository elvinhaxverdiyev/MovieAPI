from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAuthenticated, BasePermission
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from django.core.mail import send_mail

from django.conf import settings
from users.serializers import *
from movieapp.models import *
from movieapp.serializers import *
from users.models import *
from notifications.sendmail import send_movie_created_email

# Create your views here.

class HeHasPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user or request.user.is_staff
    

class UserListAPIView(APIView):
    """APIView to list all users."""
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get(self, request, *args, **kwargs):
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRegisterAPIView(APIView):
    """APIView for user registration."""
    permission_classes = [AllowAny] 

    def post(self, request, *args, **kwargs):
        """Handle POST requests to create a new user."""
        serializer = CustomUserRegisterSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save() 
            token, created = Token.objects.get_or_create(user=user)  
            return Response({
                "message": "Profile created successfully",
                "username": user.username,
                "email": user.email,
                "token": token.key
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class LogInAPIView(APIView):
    """Users login APi method"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"] 
            token, created = Token.objects.get_or_create(user=user)
            return Response({"message": "Login successful", "token": token.key
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
class AccountDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = CustomUserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        serializer = CustomUserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if not user.check_password(serializer.validated_data["old_password"]):
                return Response({"old_password": "Old password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(serializer.validated_data["new_password"])
            user.save()
            return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserLogoutAPIView(APIView):
    """APIView for user logout."""
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        """Handle POST requests to log out a user."""
        try:
            token = Token.objects.get(user=request.user)
            token.delete() 
            return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
        

class MoviePagination(PageNumberPagination):
    """Pagination class that splits the movie list into pages."""
    page_size = 2
    

class MovieListPostAPIView(APIView):
    """API that retrieves a list of movies and allows adding new ones."""
    
    permission_classes = [AllowAny]  
    pagination_class = MoviePagination
    
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
    
