from django.urls import path

from . import views

urlpatterns = [
    path('fill', views.fill_national),
    path('lc_fill', views.fill_lc),
    path('final_lc_fill', views.fill_lc_final),
    path('calc', views.calc),
    path('reset_changes', views.reset_changes),
    path('reset_ratings', views.reset_ratings),
    path('reset_matches', views.reset_matches),
    path('test_ratings', views.test_ratings),
    path('rating', views.show_rating),
    path('rating/<int:champ_id>', views.show_rating_by_champ,),
    path('country_rating', views.show_country_rating),
    path('top_changes', views.top_delta),
    path('top_rating_ever', views.top_rating_ever),
    path('get_chart', views.get_chart),
    path('charts', views.charts),
    path('fill_change_position', views.fill_change_position),
    path('get_position_charts', views.get_position_chart),
    path('position_charts', views.position_charts),
    path('position_continuity', views.position_continuity),
]