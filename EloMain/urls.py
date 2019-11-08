from django.urls import path

from . import views

urlpatterns = [
    path('fill', views.fill_national),
    path('lc_fill', views.fill_lc),
    path('final_lc_fill', views.fill_lc_final)
]