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
    path('country_rating', views.show_country_rating),
]