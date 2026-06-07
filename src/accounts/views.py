from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from .forms import UserRegisterForm

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect ("home:index")
    else:
        form = UserRegisterForm()

    return render(
        request,
        "accounts/register.html",
        {'form': form},
    )

def logout_view(request):
    logout(request)
    return redirect('home:index')


@login_required
def profile(request):
    favorites_count = request.user.favorites.count()

    return render(
        request,
        "accounts/profile.html",
        {
            "fovorites_count": favorites_count,
        }
    )