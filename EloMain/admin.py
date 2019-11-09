from django.contrib import admin

# Register your models here.
from .models import Championship, Club, Game

class ClubAdmin(admin.ModelAdmin):
    list_filter = ('championship', )
    search_fields = ('name', )

class GameAdmin(admin.ModelAdmin):
    list_filter = ('tournament',)

admin.site.register(Championship)
admin.site.register(Club, ClubAdmin)
admin.site.register(Game, GameAdmin)

