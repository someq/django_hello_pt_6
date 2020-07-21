from django.shortcuts import render


def index_view(request):
    return render(request, 'index.html')


def article_create_view(request):
    if request.method == "GET":
        return render(request, 'article_create.html')
    elif request.method == 'POST':
        context = {
            'title': request.POST.get('title'),
            'content': request.POST.get('content'),
            'author': request.POST.get('author')
        }
        return render(request, 'article_view.html', context)
