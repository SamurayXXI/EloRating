from django.contrib import admin

# Register your models here.
from .filters import LastMonthFilter
from .models import Championship, Club, Game, Change, Position, Options


class ClubAdmin(admin.ModelAdmin):
    list_display = ("name", "rating")
    list_filter = ("championship",)
    search_fields = ("name",)


class GameAdmin(admin.ModelAdmin):
    list_filter = ("tournament",)


class ChangeAdmin(admin.ModelAdmin):
    search_fields = ("club__name",)
    list_filter = (LastMonthFilter,)
    list_display = ("game", "club", "rating_delta", "rating_before", "rating_after")
    list_filter = ("game__date",)


admin.site.register(Championship)
admin.site.register(Club, ClubAdmin)
admin.site.register(Game, GameAdmin)
admin.site.register(Change, ChangeAdmin)
admin.site.register(Position)
admin.site.register(Options)
