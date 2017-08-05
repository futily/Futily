from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'username', 'is_active', 'is_staff']
    raw_id_fields = ['favourite_player', 'favourite_club', 'favourite_nation']
    search_fields = ['email', 'username']

    fieldsets = [
        (None, {
            'fields': ['email', 'username', 'password', 'is_active', 'is_staff'],
        }),
        ('About', {
            'fields': ['about_me', 'preferred_platform'],
        }),
        ('Gamertags', {
            'fields': ['psn', 'xbox', 'origin'],
        }),
        ('Social accounts', {
            'fields': ['twitter', 'youtube', 'twitch', 'facebook'],
        }),
        ('Favourites', {
            'fields': ['favourite_player', 'favourite_club', 'favourite_nation'],
        }),
    ]

    add_fields = [
        (None, {
            'classes': ['wide'],
            'fields': ['email', 'username', 'password1', 'password2'],
        }),
    ]
