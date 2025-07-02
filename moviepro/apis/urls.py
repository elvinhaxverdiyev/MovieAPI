from django.urls import path
from .auth_apis import *
from .views import *
from .movie_control import *
from .interactions_api import *


urlpatterns = [
    path(
        'register/',
        UserRegisterAPIView.as_view(),
        name="register"
    ),
    path(
        'login/',
        LogInAPIView.as_view(),
        name="login"
    ),
    path(
        'account/',
        AccountDetailAPIView.as_view(),
        name="account-detail"
    ),
    path(
        'account/change-password/',
        ChangePasswordAPIView.as_view(),
        name="change-password"
    ),  
    path('logout/',
         UserLogoutAPIView.as_view(),
         name="logout"
    ),
    path(
        'users/',
        UserListAPIView.as_view(),
        name="user-list"
    ),
    path(
        'movies/',
        MovieListPostAPIView.as_view(),
        name="movie-list"
    ),
    path(
        'movies/<int:id>/',
        MovieDetailAPIView.as_view(),
        name="movie-detail"
    ),
    path(
        'movies/<int:id>/like/',
        MovieLikeAPIView.as_view(), 
        name="movie-like"
    ),
    path(
        'movies/<int:id>/comments/',
        AddCommentAPIView.as_view(),
        name="add-comment"
    ),
    path(
        'comments/<int:id>/delete/',
        DeleteCommentAPIView.as_view(),
        name="delete-comment"
    ),
    path(
        'movies/search/',
        MovieSearchAPIView.as_view(),
        name="movie-search"
    ),
    path(
        'movies/by_genre/',
        MovieByGenreAPIView.as_view(),
        name="movies-by-genre"
    ),
    path(
        'genres/',
        GenreListAPIView.as_view(),
        name="genre-list"
    )
]
