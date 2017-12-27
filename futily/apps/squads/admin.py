from django.contrib import admin

from .models import Squad


@admin.register(Squad)
class SquadAdmin(admin.ModelAdmin):
    pass
