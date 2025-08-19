from django.db import models

from users.models import CustomUser
from .actors_models import Actor
from .category_models import Category


class Movie(models.Model):
    """
    Model representing a movie.

    Fields:
        title (CharField): The title of the movie (max length: 255).
        description (TextField): A detailed description or synopsis of the movie.
        poster (ImageField, optional): The main poster image of the movie, stored in 'movies/'.
        created_by (ForeignKey): The user (admin/creator) who added the movie.
        genres (ManyToManyField): Categories/genres associated with the movie.
        actors (ManyToManyField): Actors who played in the movie.
        trailer_link (URLField, optional): A link to the trailer (e.g., YouTube).
        likes (ManyToManyField): Users who liked the movie.
        views_count (PositiveIntegerField): Number of times the movie was viewed.
        created_at (DateTimeField): Timestamp when the movie record was created.

    Relations:
        - `created_by` → CustomUser
        - `genres` → Category (many-to-many)
        - `actors` → Actor (many-to-many)
        - `likes` → CustomUser (many-to-many)

    Methods:
        __str__(): Returns the movie title as its string representation.
    """
    title = models.CharField(max_length=255)
    description = models.TextField()
    poster = models.ImageField(upload_to="movies/", null=True, blank=True) 
    created_by = models.ForeignKey(
        CustomUser,
        related_name="created_movies",
        on_delete=models.CASCADE
    )
    genres = models.ManyToManyField(Category, related_name="movies")
    actors = models.ManyToManyField(Actor, related_name="movies")
    trailer_link = models.URLField(blank=True)
    likes = models.ManyToManyField(CustomUser, related_name="liked_movies", blank=True)
    views_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title