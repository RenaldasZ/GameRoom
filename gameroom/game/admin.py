from django.contrib import admin
from . import models 

# Register your models here.

class PlayerAdmin(admin.ModelAdmin):
    list_display = ('user', 'score', 'played')
    list_filter = ('score', 'user', 'played')


admin.site.register(models.Player, PlayerAdmin)
admin.site.register(models.Match)
