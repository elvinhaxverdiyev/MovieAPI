from django.db import models


class Category(models.Model):
    """
    Model representing a category.

    Fields:
        name (str): The unique name of the category (max length: 100).

    Methods:
        __str__(): Returns the category name as its string representation.
    """
    name = models.CharField(max_length=100, unique=True)  

    def __str__(self):
        return self.name
    