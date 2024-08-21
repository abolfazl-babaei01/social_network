from django.contrib import admin
from .models import SocialUser, Contact
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
