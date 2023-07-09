from django.contrib import admin

# Register your models here.
from src.apps.post.models import Post, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        
        "description", 
        "author", 
        "created_at",
        "updated_at", 
        "is_archived",
        "display_image",
        ]
    
    list_filter = [
        "created_at",
        "is_archived"
    ]
    search_fields = [
        "description",
        "author__username",
    ]
    def display_image(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" width="50" height="50" />'
    display_image.short_description = 'Изображение'


    admin.site.register(Comment)