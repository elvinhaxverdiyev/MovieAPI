from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("username", "email", "is_staff", "is_active", "bio_snippet", "image_preview")
    list_filter = ("is_staff", "is_active")
    search_fields = ("username", "email", "bio")
    ordering = ("username",)
    
    fieldsets = UserAdmin.fieldsets + (
        (None, {"fields": ("bio", "image")}),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height: 50px; border-radius: 50%;" />', obj.image.url)
        return "Şəkil yoxdur"
    image_preview.short_description = 'Profil Şəkli'

    def bio_snippet(self, obj):
        return obj.bio[:50] + '...' if obj.bio else "No bio"
    bio_snippet.short_description = 'Bio Snippet'

admin.site.register(CustomUser, CustomUserAdmin)
