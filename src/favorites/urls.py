from django.urls import path
from . import views

app_name = "favorites" 

urlpatterns = [
    path("", views.list_favorites, name="list_favorites"),
    path("add/", views.add_favorite, name="add_favorite"),
    path("delete/<int:id>/", views.delete_favorite, name="delete_favorite"),
]