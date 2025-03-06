from django.contrib import admin
from .models import *
from django.utils.html import format_html

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1  # Yeni şərh əlavə etmək üçün boş sahə göstər

class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'created_by', 'actor_count', 'movie_image_preview', 'views_count', 'like_count')
    list_filter = ('genres', 'created_at', 'actors')  # Filmlər üzrə kateqoriya, yaradılma tarixi, aktyorlar ilə filtr tətbiq et
    search_fields = ('title', 'description', 'actors__name', 'created_by__username')  # Axtarış sahələri
    ordering = ('-created_at',)  # Ən son əlavə edilən filmlər ilk sıralanacaq
    inlines = [CommentInline]  # Şərh sahəsini inline olaraq əlavə edirik

    # Aktyorların sayını göstərmək üçün metod
    def actor_count(self, obj):
        return obj.actors.count() if obj.actors.exists() else 0
    actor_count.short_description = 'Aktyor Sayı'

    # Filmin şəkilini önizləmək üçün metod
    def movie_image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 100px; height: auto;" />', obj.image.url)
        return "Şəkil yoxdur"
    movie_image_preview.short_description = 'Film Şəkli'

    # Filmin bəyənmə sayını göstərmək üçün metod
    def like_count(self, obj):
        return obj.likes.count()
    like_count.short_description = 'Bəyənmə Sayı'

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Kateqoriyaların adını göstər
    search_fields = ('name',)  # Kateqoriya adında axtarış et
    ordering = ('name',)  # Kateqoriyaları adı ilə sıralayır

class ActorAdmin(admin.ModelAdmin):
    list_display = ('name', 'movies_count')  # Aktyor adı, doğum tarixi və filmlərini göstər
    search_fields = ('name',)
    ordering = ('name',)  # Aktyorları adı ilə sıralayır

    def movies_count(self, obj):
        return obj.movies.count()
    movies_count.short_description = 'Filmlər'

class MovieLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'movie', 'created_at')  # Bəyənmə məlumatlarını göstər
    search_fields = ('user__username', 'movie__title')  # İstifadəçi adı və film başlığı ilə axtarış et
    list_filter = ('created_at',)  # Tarix üzrə filtr tətbiq et
    ordering = ('-created_at',)  # Ən son bəyənmələri göstər

class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'movie', 'text', 'created_at')  # Şərhləri göstərmək üçün sahələr
    search_fields = ('user__username', 'movie__title', 'text')  # Axtarış sahələri
    list_filter = ('created_at',)  # Tarix üzrə filtr tətbiq et
    ordering = ('-created_at',)  # Ən son şərhləri göstər

# Admin panelinə modelləri əlavə edirik
admin.site.register(Movie, MovieAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Actor, ActorAdmin)
admin.site.register(MovieLike, MovieLikeAdmin)
admin.site.register(Comment, CommentAdmin)
