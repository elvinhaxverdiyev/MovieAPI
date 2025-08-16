from django.db import models


class Actor(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(max_length=2500, blank=True, null=True)
    image = models.ImageField(upload_to="actors/", null=True, blank=True)  

    def __str__(self):
        return self.name
