from django.shortcuts import render
from common.utils import fetch_quote

# List of tags can be a module-level constant if you like
all_tags = [
    "Anxiety","Change","Choice","Confidence","Courage","Death","Dreams",
    "Excellence","Failure","Fairness","Fear","Forgiveness","Freedom",
    "Future","Happiness","Inspiration","Kindness","Leadership","Life",
    "Living","Love","Pain","Past","Success","Time","Today","Truth","Work"
]

def index(request):
    """
    Main page view. If GET parameters include 'keyword' or 'author',
    fetch a quote and pass it to the template.
    """
    popular_tags = all_tags[:8]
    keyword = request.GET.get('keyword')
    author = request.GET.get('author')
    quote = fetch_quote(keyword=keyword, author=author)

    context = {
        'tags': popular_tags,
        'quote': quote,
        'error_message': None if quote else ("No quote found matching your criteria" if keyword or author else None)
    }

    return render(request, "home/index.html", context)


def quote_partial(request):
    keyword = request.GET.get("keyword")
    quote = fetch_quote(keyword=keyword)

    return render(
        request, 
        "home/partials/_quote_card.html",
        {
            "quote": quote, 
            "active_tag": keyword,
            "error_message": None if quote else "No quote found"
        },
    )


def inspire(request):
    quote = fetch_quote(use_cache=False)  # Force fetch a new quote, bypassing cache

    return render(
        request,
        "home/partials/_quote_card.html",
        {
            "quote": quote,
            "error_message": None if quote else "No quote found",
        },
    )