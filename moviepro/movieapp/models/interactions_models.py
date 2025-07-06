from django.db import models

from users.models import CustomUser
from .movie_models import Movie



class MovieLike(models.Model):
    user = models.ForeignKey(CustomUser, null=True, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "movie")  

    def __str__(self):
        user_name = self.user.username if self.user else "Anonymous"
        return f"{user_name} liked {self.movie.title}"

    
class Comment(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"
