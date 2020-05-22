from django.urls import path

from . import views

urlpatterns = [
    path("fill", views.fill_national),
    path("lc_fill", views.fill_lc),
    path("final_lc_fill", views.fill_lc_final),
    path("calc", views.calc),
    path("reset_changes", views.reset_changes),
    path("reset_ratings", views.reset_ratings),
    path("reset_matches", views.reset_matches),
    path("test_ratings", views.test_ratings),
    # path("rating", views.show_rating),
    path("rating/<int:champ_id>", views.show_rating_by_champ,),
    path("country_rating", views.show_country_rating),
    path("top_changes", views.top_delta),
    path("top_rating_ever", views.top_rating_ever),
    path("get_chart", views.get_chart),
    path("charts", views.charts),
    path("fill_change_position", views.fill_change_position),
    path("get_position_charts", views.get_position_chart),
    path("position_charts", views.position_charts),
    path("position_continuity", views.position_continuity),
    path("panel", views.panel),
    path("last_matches_fill", views.fill_last_matches),
    path("month_rating", views.month_rating),
    path("year_rating", views.year_rating),
    path("last_changes", views.last_changes),
    path("", views.index, name="index"),
    path("rating", views.rating, name="rating"),
    path("country/<int:champ_id>", views.country_clubs),
    path("country", views.country, name="country"),
    path("matches", views.matches, name="matches"),
    path("tops", views.tops, name="tops"),
    path("calculator", views.calculator, name="calculator"),
    path("celery_sum", views.celery_sum)
]
