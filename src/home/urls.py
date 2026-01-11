from django.urls import path
from . import views 

appname = "home"
urlpatterns = [
    path("", views.index, name="index"),
    path("quote/", views.quote_partial, name="quote-partial"),
    path("inspire-me/", views.inspire, name="inspire-me"),
]



