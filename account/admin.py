from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from .forms import CreateSocialUserForm, EditSocialUserForm


# Register your models here.
@admin.register(SocialUser)
class SocialUserAdmin(UserAdmin):
    add_form = CreateSocialUserForm
    form = EditSocialUserForm
    model = SocialUser
    list_display = ['username', 'first_name', 'last_name', 'email', 'is_active']
    list_editable = ['is_active']
    search_fields = ['username']
    list_filter = ['is_deleted']

    fieldsets = (
        (None, {'fields': ('username', 'phone', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions',
         {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_deleted', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Additional Info', {'fields': ('avatar', 'job', 'bio', 'date_of_birth', 'reason_deleting_account')})
    )

    add_fieldsets = (
        (None, {'fields': ('username', 'phone', 'password1', 'password2')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions',
         {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_deleted', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Additional Info', {'fields': ('avatar', 'job', 'bio', 'date_of_birth', 'reason_deleting_account')})
    )


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['user_from', 'user_to']
