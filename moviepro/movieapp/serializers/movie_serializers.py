from rest_framework import serializers

from movieapp.models.movie_models import Movie
from movieapp.models.interactions_models import MovieLike
from movieapp.models.actors_models import Actor
from movieapp.models.category_models import Category
from movieapp.serializers.image_serializers import ImageSerializer


class MovieSerializer(serializers.ModelSerializer):
    """
    Serializer for retrieving movie details.

    - Includes basic fields such as title, description, trailer link, and views count.
    - Adds calculated fields:
        * `like_count`: Number of likes for the movie.
        * `poster`: Full absolute URL of the poster.
        * `extra_images`: Related images of the movie.
    """
    like_count = serializers.SerializerMethodField()
    poster = serializers.SerializerMethodField()
    extra_images = ImageSerializer(many=True, read_only=True)

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
            "poster",
            "extra_images",
            "genres"
        ]

    def get_poster(self, obj):
        """Return absolute URI for the movie poster if available."""
        if obj.poster:
            try:
                request = self.context["request"]  
                return request.build_absolute_uri(obj.poster.url)
            except KeyError: 
                return obj.poster.url
        return None


    def get_like_count(self, obj):
         """Return total number of likes for the movie."""
         return MovieLike.objects.filter(movie=obj).count()


class MovieCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new movie.

    - Accepts `genres` and `actors` as lists of names (strings).
    - Automatically creates `Category` and `Actor` objects if they do not exist.
    - Handles optional poster image upload.
    - Provides read-only display fields for genres and actors.
    """
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
            "poster",  
        ]
    
    
    def create(self, validated_data):
        """
        Create a new Movie instance with associated genres and actors.

        - Extracts `genres` and `actors` from input.
        - Ensures that related Category and Actor objects exist.
        - Assigns poster image if provided.
        """
        genres = validated_data.pop("genres", [])
        actors_list = validated_data.pop("actors", [])
        image = validated_data.pop("poster", None)  
        movie = Movie.objects.create(**validated_data)

        for genre_name in genres:
            genre, created = Category.objects.get_or_create(name=genre_name)
            movie.genres.add(genre)

        for actor_name in actors_list:
            actor, created = Actor.objects.get_or_create(name=actor_name)
            movie.actors.add(actor)
        if image:
            movie.poster = image
            movie.save()

        return movie

    def get_genres_display(self, obj):
        """Return a list of genre names related to the movie."""
        return [genre.name for genre in obj.genres.all()]

    def get_actors_display(self, obj):
        """Return a list of actor names related to the movie."""
        return [actor.name for actor in obj.actors.all()]


class MovieUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating an existing movie.

    - Allows partial update of movie fields such as title, description, trailer link, etc.
    - Handles updating many-to-many relationships for actors and genres.
    - Includes read-only likes_count field.
    """
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