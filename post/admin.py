from django.contrib import admin
from .models import Post, Image, Comment


# Register your models here.

class ImageInline(admin.StackedInline):
    model = Image
    extra = 0


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'created_at', 'is_published']
    inlines = [ImageInline]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'post', 'is_published']
    list_editable = ['is_published']