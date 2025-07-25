from rest_framework import serializers

from movieapp.models.movie_models import Movie
from movieapp.models.interactions_models import MovieLike
from movieapp.models.actors_models import Actor
from movieapp.models.category_models import Category


class MovieSerializer(serializers.ModelSerializer):
    like_count = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = [
            "id",
            "title",
            "description",
            "actors",
            "trailer_link",
            "views_count",
            "like_count",
            "image",
        ]

    def get_image(self, obj):
        if obj.image:
            try:
                request = self.context["request"]  
                return request.build_absolute_uri(obj.image.url)
            except KeyError: 
                return obj.image.url
        return None


    def get_like_count(self, obj):
         return MovieLike.objects.filter(movie=obj).count()


class MovieCreateSerializer(serializers.ModelSerializer):
    genres = serializers.ListField(child=serializers.CharField(), write_only=True)
    actors = serializers.ListField(child=serializers.CharField(), write_only=True)
    genres_display = serializers.SerializerMethodField(read_only=True)
    actors_display = serializers.SerializerMethodField(read_only=True)
    image = serializers.ImageField(write_only=True, required=False) 

    class Meta:
        model = Movie
        fields = [
            "title",
            "description",
            "genres",
            "actors",
            "genres_display",
            "actors_display",
            "image",  
        ]
    
    def create(self, validated_data):
        genres = validated_data.pop("genres", [])
        actors_list = validated_data.pop("actors", [])
        image = validated_data.pop("image", None)  
        movie = Movie.objects.create(**validated_data)

        for genre_name in genres:
            genre, created = Category.objects.get_or_create(name=genre_name)
            movie.genres.add(genre)

        for actor_name in actors_list:
            actor, created = Actor.objects.get_or_create(name=actor_name)
            movie.actors.add(actor)
        if image:
            movie.image = image
            movie.save()

        return movie

    def get_genres_display(self, obj):
        return [genre.name for genre in obj.genres.all()]

    def get_actors_display(self, obj):
        return [actor.name for actor in obj.actors.all()]


class MovieUpdateSerializer(serializers.ModelSerializer):
    likes_count = serializers.IntegerField(read_only=True)
    actors = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Actor.objects.all(),
        required=False
    )
    genres = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset= Category.objects.all(),
        required=False
    )

    class Meta:
        model = Movie
        fields = [
            "title",
            "description",
            "actors",
            "trailer_link",
            "genres",
            "views_count",
            "likes_count"
        ]

    def update(self, instance, validated_data):
        instance.title = validated_data.get("title", instance.title)
        instance.description = validated_data.get("description", instance.description)
        instance.trailer_link = validated_data.get("trailer_link", instance.trailer_link)
        instance.views_count = validated_data.get("views_count", instance.views_count)
        actors_data = validated_data.get("actors")
        
        if actors_data is not None:
            instance.actors.set(actors_data)

        genres_data = validated_data.get("genres")
        if genres_data is not None:
            instance.genres.set(genres_data)
        instance.save()
        return instance