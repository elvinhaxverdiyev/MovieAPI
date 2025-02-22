from django.urls import path
from .views import *

urlpatterns = [
    path('movies/', MovieListPostView.as_view(), name="movie-list"),
    path('movies/<int:id>/', MovieDetailView.as_view(), name="movie-detail"),
    path('movies/<int:id>/like/', MovieLikeView.as_view(), name="movie-like"),
    path('movies/<int:id>/unlike/', MovieUnlikeView.as_view(), name="movie-unlike"),
    path('movies/<int:id>/comments/', AddCommentView.as_view(), name="add-comment"),
    path('comments/<int:id>/delete/', DeleteCommentView.as_view(), name="delete-comment"),
    path('movies/search/', MovieSearchView.as_view(), name="movie-search"),
]
