from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("api/health/", views.health, name="api_health"),
    path("api/check/", views.check_numbers, name="api_check"),
    path("api/suggest/coverage/", views.suggest_coverage, name="api_suggest_coverage"),
    path("api/suggest/top-stat/", views.suggest_top_stat, name="api_suggest_top_stat"),
    path("api/suggest/diverse/", views.suggest_diverse, name="api_suggest_diverse"),
]
