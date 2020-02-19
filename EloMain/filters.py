from datetime import date
from django.contrib.admin import SimpleListFilter
from django.db.models import Q


class LastMonthFilter(SimpleListFilter):
    title = "По последнему месяцу"

    parameter_name = "game__date"

    def lookups(self, request, model_admin):
        return (
            ("all_clubs", "Все клубы"),
            ("top_clubs", "Топ клубы"),
            ("russian_clubs", "Россия"),
            ("england_clubs", "Англия"),
        )

    def queryset(self, request, queryset):
        if self.value() == "all_clubs":
            date1 = date.today()
            return queryset.filter(
                game__date__gte=date(date1.year, date1.month - 1, 1), game__date__lt=date(date1.year, date1.month, 1)
            )
        if self.value() == "top_clubs":
            date1 = date.today()
            return queryset.filter(
                game__date__gte=date(date1.year, date1.month - 1, 1),
                game__date__lt=date(date1.year, date1.month, 1),
                rating_after__gte=1200,
            )
        if self.value() == "russian_clubs":
            date1 = date.today()
            return queryset.filter(
                game__date__gte=date(date1.year, date1.month - 1, 1), game__date__lt=date(date1.year, date1.month, 1)
            ).filter(Q(game__home_team__championship__name="Россия") | Q(game__away_team__championship__name="Россия"))
        if self.value() == "england_clubs":
            date1 = date.today()
            return queryset.filter(
                game__date__gte=date(date1.year, date1.month - 1, 1), game__date__lt=date(date1.year, date1.month, 1)
            ).filter(Q(game__home_team__championship__name="Англия") | Q(game__away_team__championship__name="Англия"))
