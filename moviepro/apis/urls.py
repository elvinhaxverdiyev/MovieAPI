from django.urls import path
from .views import *

urlpatterns = [
    path('movies/', MovieListPostAPIView.as_view(), name="movie-list"),
    path('movies/<int:id>/', MovieDetailAPIView.as_view(), name="movie-detail"),
    path('movies/<int:id>/like/', MovieLikeAPIView.as_view(), name="movie-like"),
    path('movies/<int:id>/unlike/', MovieUnlikeAPIView.as_view(), name="movie-unlike"),
    path('movies/<int:id>/comments/', AddCommentAPIView.as_view(), name="add-comment"),
    path('comments/<int:id>/delete/', DeleteCommentAPIView.as_view(), name="delete-comment"),
    path('movies/search/', MovieSearchAPIView.as_view(), name="movie-search"),
]
