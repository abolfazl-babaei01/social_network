from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin


# Register your models here.
@admin.register(SocialUser)
class SocialUserAdmin(admin.ModelAdmin):
    list_display = ['username', 'first_name', 'last_name', 'email', 'is_active']
    list_editable = ['is_active']
    fieldsets = UserAdmin.fieldsets + (
        (
            'Additional Info', {'fields': ('date_of_birth', 'avatar', 'job', 'bio', 'phone')}),
    )


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['user_from', 'user_to',]


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at', 'is_expired']
    list_filter = ['user']
