from django.contrib import admin
from taggit.models import Tag

from .models import *


# Register your models here.

class ImageInline(admin.StackedInline):
    model = Image
    extra = 0


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'created_at', 'is_published']
    inlines = [ImageInline]
    list_filter = ['author']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author', 'post', 'is_published']
    list_editable = ['is_published']



class StoryVisitInline(admin.StackedInline):
    model = StoryVisit
    extra = 0

@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at','is_delete', 'is_expired']
    list_filter = ['user']
    list_editable = ['is_delete']
    autocomplete_fields = ['user']
    inlines = [StoryVisitInline]


@admin.register(StoryVisit)
class StoryVisitAdmin(admin.ModelAdmin):
    list_display = ['story', 'user', 'ip']