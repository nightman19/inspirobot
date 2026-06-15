from django.urls import path

from .views import settings_view


app_name = "settings"


urlpatterns = [
    path("", settings_view, name="index"),
]