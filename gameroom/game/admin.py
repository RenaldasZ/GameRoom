from django.contrib import admin
from . import models 

# Register your models here.

class PlayerAdmin(admin.ModelAdmin):
    list_display = ('user', 'score', 'played')
    list_filter = ('score', 'user', 'played')

class MatchsAdmin(admin.ModelAdmin):
    list_display = ('id', 'player1', 'player2', 'played_at')

admin.site.register(models.Player, PlayerAdmin)
admin.site.register(models.Match, MatchsAdmin)
