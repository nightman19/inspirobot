from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout

from .forms import UserRegisterForm

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            messages.success(
                request,
                f"🎉 Welcome to Inspirobot, {user.username}!"
            )

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

    messages.info(
        request,
        "You've been logged out successfully."
    )

    return redirect('home:index')


