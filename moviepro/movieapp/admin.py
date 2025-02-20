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
