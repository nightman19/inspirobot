from django.shortcuts import render
from common.utils import fetch_quote


def index(request):
    tags = ["Anxiety","Change","Choice","Confidence","Courage","Death","Dreams","Excellence","Failure","Fairness","Fear","Forgiveness","Freedom","Future","Happiness","Inspiration","Kindness","Leadership","Life","Living","Love","Pain","Past","Success","Time","Today","Truth","Work"]
    context = {'tags': tags}
    return render(request, "home/index.html", context)


def quotes_view(request):
    keyword = request.GET.get('keyword') # Get keywprd from query string (if applicable)
    author = request.GET.get('author') # Get author from query string (if applicable)
    quote = fetch_quote(keyword=keyword, author=author)

    if quote:
        context = {'quote': quote}
        return render(request, 'home/inspirobot.html', context)
    else:
        context = {'error_message': "No quote found matchin your criteria" }
        return render(request, 'home/inspirobot.html', context)
        