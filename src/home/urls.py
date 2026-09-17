from django.urls import path
from . import views

app_name = "home"

urlpatterns = [
    path("", views.index, name="index"),
    path("quote/", views.quote_partial, name="quote-partial"),
    path("inspire-me/", views.inspire, name="inspire-me"),
    path("share-card/", views.share_card_image, name="share-card"),
    path("share-link/", views.share_link, name="share-link"),
    path("q/<str:short_id>/", views.quote_detail, name="quote-detail"),
]