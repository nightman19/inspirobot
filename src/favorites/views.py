from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from .models import Favorite


@login_required
def add_favorite(request):
    if request.method == 'POST':
        quote = request.POST.get("quote")
        author = request.POST.get("author")

        favorite = Favorite.objects.filter(
            user=request.user,
            quote_text=quote,
            author=author
        ).first()

        if favorite:
            favorite.delete()

            return HttpResponse("""
                <span class="material-symbols-outlined text-slate-700 dark:text-slate-200 text-[20px]"
                    style="font-variation-settings:'FILL' 0;">
                    bookmark
                </span>
            """)
    
        Favorite.objects.create(
            user=request.user,
            quote_text=quote,
            author=author
        )

        return HttpResponse("""
            <span class="material-symbols-outlined text-slate-700 dark:text-slate-200 group-hover:scale-110 transition-transform text-[20px]"
                style="font-variation-settings:'FILL' 1;">
                bookmark
            </span>
        """)
    

@login_required
def list_favorites(request):
    favorites = Favorite.objects.filter(user=request.user).order_by("-created_at")

    return render(
        request, 
        "favorites/list.html",
        {"favorites": favorites}
    )


@login_required
def delete_favorite(request, id):
    favorite = Favorite.objects.get(id=id, user=request.user)
    favorite.delete()

    return HttpResponse("")