from django.contrib import admin
from .models import *
from django.utils.html import format_html

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1  

class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'created_by', 'actor_count', 'movie_image_preview', 'views_count', 'like_count')
    list_filter = ('genres', 'created_at', 'actors') 
    search_fields = ('title', 'description', 'actors__name', 'created_by__username') 
    ordering = ('-created_at',)  
    inlines = [CommentInline]  

    def actor_count(self, obj):
        return obj.actors.count() if obj.actors.exists() else 0
    actor_count.short_description = 'Aktyor Sayı'

    def movie_image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 100px; height: auto;" />', obj.image.url)
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
    list_display = ('name', 'movies_count')  
    search_fields = ('name',)
    ordering = ('name',)  
    def movies_count(self, obj):
        return obj.movies.count()
    movies_count.short_description = 'Filmlər'

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

# Admin panelinə modelləri əlavə edirik
admin.site.register(Movie, MovieAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Actor, ActorAdmin)
admin.site.register(MovieLike, MovieLikeAdmin)
admin.site.register(Comment, CommentAdmin)
