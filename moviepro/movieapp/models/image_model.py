from django.db import models

from .actors_models import Actor
from .movie_models import Movie


class Image(models.Model):
    actor = models.ForeignKey(
        Actor,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='extra_images'
    )
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='extra_images'
    )
    image = models.ImageField(upload_to='extra/')

    def __str__(self):
        return f"Image: {self.image}"