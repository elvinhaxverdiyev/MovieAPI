from django.db import models

from users.models import CustomUser
from .movie_models import Movie



class MovieLike(models.Model):
    """
    Model representing a "like" given by a user to a movie.

    Fields:
        user (ForeignKey): The user who liked the movie. 
            If the user is deleted, related likes are deleted.
        movie (ForeignKey): The movie that was liked.
        created_at (DateTime): Timestamp when the like was created.

    Meta:
        unique_together: Ensures that the same user cannot like 
        the same movie more than once.

    Methods:
        __str__(): Returns a readable string showing who liked which movie.
    """
    user = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "movie")  

    def __str__(self):
        user_name = self.user.username if self.user else "Anonymous"
        return f"{user_name} liked {self.movie.title}"

    
class Comment(models.Model):
    """
    Model representing a comment left by a user on a movie.

    Fields:
        movie (ForeignKey): The movie on which the comment was made.
        user (ForeignKey): The user who wrote the comment.
        text (TextField): The body of the comment.
        created_at (DateTime): Timestamp when the comment was created.

    Relations:
        - Accessible from a movie instance via `movie.comments.all()`.

    Methods:
        __str__(): Returns a string showing which user commented on which movie.
    """
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"
