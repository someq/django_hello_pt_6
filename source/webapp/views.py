from django.shortcuts import render
from webapp.models import Article
from django.http import HttpResponseNotAllowed


def index_view(request):
    data = Article.objects.all()
    return render(request, 'index.html', context={
        'articles': data
    })


def article_create_view(request):
    if request.method == "GET":
        return render(request, 'article_create.html')
    elif request.method == 'POST':
        title = request.POST.get('title')
        text = request.POST.get('text')
        author = request.POST.get('author')
        article = Article.objects.create(title=title, text=text, author=author)
        context = {'article': article}
        return render(request, 'article_view.html', context)
    else:
        return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])

