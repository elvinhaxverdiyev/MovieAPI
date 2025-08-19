from django.db import models


class Actor(models.Model):
    """
    Model representing an actor.

    Fields:
        name (str): The full name of the actor (max length: 255).
        description (str, optional): A short biography or description of the actor (max length: 2500).
        image (ImageField, optional): Profile image of the actor, stored in the 'actors/' directory.

    Methods:
        __str__(): Returns the actor's name as its string representation.
    """
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=2500, blank=True, null=True)
    image = models.ImageField(upload_to="actors/", null=True, blank=True)  

    def __str__(self):
        return self.name
