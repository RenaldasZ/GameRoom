from django.contrib import admin
from .models import Player

# Register your models here.

class PlayerAdmin(admin.ModelAdmin):
    list_display = ('user', 'score')
    list_filter = ('score', 'user')


admin.site.register(Player, PlayerAdmin)