from rest_framework import serializers

from movieapp.models.category_models import Category

        
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"