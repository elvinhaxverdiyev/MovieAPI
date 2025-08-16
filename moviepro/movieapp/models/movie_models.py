from django.db import models

from users.models import CustomUser
from .actors_models import Actor
from .category_models import Category


class Movie(models.Model):
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