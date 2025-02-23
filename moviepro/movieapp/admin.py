from django.contrib import admin
from .models import *
# Register your models here.

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1  # Yeni şərh əlavə etmək üçün boş sahə göstər

class MovieAdmin(admin.ModelAdmin):
    inlines = [CommentInline]

admin.site.register(Movie, MovieAdmin)
admin.site.register(Comment)
admin.site.register(Category)
from django.contrib import admin
from movieapp.models import Movie, MovieLike

@admin.register(MovieLike)
class MovieLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'movie', 'created_at')
    search_fields = ('user__username', 'movie__title')
    list_filter = ('created_at',)
