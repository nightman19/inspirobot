from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def settings_view(request):
    return render(
        request,
        "settings/index.html",
    )

@login_required
def about_view(request):
    return render(
        request,
        "settings/about.html",
        {
            "version": "1.0.0",
        }
    )