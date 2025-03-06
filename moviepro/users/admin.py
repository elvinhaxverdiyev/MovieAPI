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
    
    # Redefining the fieldsets to include bio and image fields in the admin panel
    fieldsets = UserAdmin.fieldsets + (
        (None, {"fields": ("bio", "image")}),
    )

    # Adding a preview for the user's image in the admin panel
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height: 50px; border-radius: 50%;" />', obj.image.url)
        return "Şəkil yoxdur"
    image_preview.short_description = 'Profil Şəkli'

    # Adding a snippet of the bio to the list display
    def bio_snippet(self, obj):
        return obj.bio[:50] + '...' if obj.bio else "No bio"
    bio_snippet.short_description = 'Bio Snippet'

# Registering the CustomUser model with the updated admin
admin.site.register(CustomUser, CustomUserAdmin)
