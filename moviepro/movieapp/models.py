from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)  

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_by = models.ForeignKey(User, related_name="created_movies", 
                                   on_delete=models.CASCADE,
                                   default=1
                                   )  
    genres = models.ManyToManyField(Category, related_name="movies")  
    actors = models.TextField()
    trailer_link = models.URLField(blank=True)
    likes = models.ManyToManyField(User, related_name="liked_movies", blank=True) 
    views_count = models.PositiveIntegerField(default=0) 

    def __str__(self):
        return self.title


class MovieLike(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "movie")  

    def __str__(self):
        user_name = self.user.username if self.user else "Anonymous"
        return f"{user_name} liked {self.movie.title}"

    
    
    
class Comment(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"
