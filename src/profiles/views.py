from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from favorites.models import Favorite

@login_required
def profile(request):
    favorites_count = Favorite.objects.filter(
        user=request.user
    ).count()

    print("Favorites:", favorites_count)

    return render(
        request,
        "profiles/profile.html",
        {
            "favorites_count": favorites_count,
        }
    )