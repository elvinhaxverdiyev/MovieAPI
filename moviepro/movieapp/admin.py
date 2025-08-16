from django.contrib import admin
from django.utils.html import format_html
from .models import *


# ==== INLINE-lar ====

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1  


class ImageInline(admin.TabularInline):
    model = Image
    extra = 1
    fields = ("image",)
    show_change_link = True


# ==== ADMINS ====

class MovieAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'description',
        'created_by',
        'actor_count',
        'movie_image_preview',
        'views_count',
        'like_count'
    )
    list_filter = ('genres', 'created_at', 'actors')
    search_fields = ('title', 'description', 'actors__name', 'created_by__username')
    ordering = ('-created_at',)
    inlines = [CommentInline, ImageInline]   # həm Comment, həm də Image inline

    def actor_count(self, obj):
        return obj.actors.count()
    actor_count.short_description = 'Aktyor Sayı'

    def movie_image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 100px; height: auto; border-radius:5px;" />',
                obj.image.url
            )
        return "Şəkil yoxdur"
    movie_image_preview.short_description = 'Film Şəkli'

    def like_count(self, obj):
        return obj.likes.count()
    like_count.short_description = 'Bəyənmə Sayı'


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)


class ActorAdmin(admin.ModelAdmin):
    list_display = ('name', 'movies_count', 'actor_image_preview')
    search_fields = ('name',)
    ordering = ('name',)
    inlines = [ImageInline]  # aktyorun əlavə şəkilləri inline

    def movies_count(self, obj):
        return obj.movies.count()
    movies_count.short_description = 'Filmlər'

    def actor_image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 80px; height: auto; border-radius:5px;" />',
                obj.image.url
            )
        return "Şəkil yoxdur"
    actor_image_preview.short_description = 'Əsas Şəkil'


class MovieLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'movie', 'created_at')
    search_fields = ('user__username', 'movie__title')
    list_filter = ('created_at',)
    ordering = ('-created_at',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'movie', 'text', 'created_at')
    search_fields = ('user__username', 'movie__title', 'text')
    list_filter = ('created_at',)
    ordering = ('-created_at',)


class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'actor', 'movie', 'image')
    search_fields = ('actor__name', 'movie__title')


# ==== REGISTER ====

admin.site.register(Movie, MovieAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Actor, ActorAdmin)
admin.site.register(MovieLike, MovieLikeAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Image, ImageAdmin)
