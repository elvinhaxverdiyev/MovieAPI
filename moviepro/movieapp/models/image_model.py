from django.db import models

from .actors_models import Actor
from .movie_models import Movie


class Image(models.Model):
    """
    Model representing additional images for actors or movies.

    Fields:
        actor (ForeignKey): Optional relation to an Actor. 
            If the actor is deleted, related images will also be deleted.
        movie (ForeignKey): Optional relation to a Movie.
            If the movie is deleted, related images will also be deleted.
        image (ImageField): The uploaded image stored in the 'extra/' directory.

    Notes:
        - Either `actor` or `movie` should typically be set to associate 
          the image with the corresponding entity.
        - The `related_name='extra_images'` allows reverse access 
          via `actor.extra_images.all()` or `movie.extra_images.all()`.

    Methods:
        __str__(): Returns a string with the image file path.
    """
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