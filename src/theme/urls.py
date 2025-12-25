from django.urls import path

from . import views

appname = "theme"
urlpatterns = [
    path("", views.index, name="index"),
    
]
