from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", include("home.urls")),
    path("favorites/", include("favorites.urls")),
    path("accounts/", include("accounts.urls")),
    path('accounts/', include('django.contrib.auth.urls')),
    path("__reload__/", include("django_browser_reload.urls")),
    path('admin/', admin.site.urls),
]
