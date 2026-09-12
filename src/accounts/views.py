from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.utils.http import url_has_allowed_host_and_scheme

from .forms import UserRegisterForm

def register(request):
    next_url = request.POST.get('next') or request.GET.get('next', '')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)

            messages.success(
                request,
                f"🎉 Welcome to Inspirobot, {user.username}!"
            )

            if next_url and url_has_allowed_host_and_scheme(
                url=next_url,
                allowed_hosts={request.get_host()},
                require_https=request.is_secure(),
            ):
                return redirect(next_url)
            return redirect ("home:index")
    else:
        form = UserRegisterForm()

    return render(
        request,
        "accounts/register.html",
        {'form': form, 'next': next_url},
    )

def logout_view(request):
    logout(request)

    messages.info(
        request,
        "You've been logged out successfully."
    )

    return redirect('home:index')


