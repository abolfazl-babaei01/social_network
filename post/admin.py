from django.contrib import admin
from .models import Post, Image


# Register your models here.

class ImageInline(admin.StackedInline):
    model = Image
    extra = 0


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'created_at', 'is_published']
    inlines = [ImageInline]