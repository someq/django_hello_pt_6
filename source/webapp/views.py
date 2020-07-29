from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotAllowed
from django.utils.timezone import make_naive

from webapp.models import Article
from .forms import ArticleForm, BROWSER_DATETIME_FORMAT


def index_view(request):
    is_admin = request.GET.get('is_admin', None)
    if is_admin:
        data = Article.objects.all()
    else:
        data = Article.objects.filter(status='moderated')
    return render(request, 'index.html', context={
        'articles': data
    })


def article_view(request, pk):
    # try:
    #     article = Article.objects.get(pk=pk)
    # except Article.DoesNotExist:
    #     raise Http404

    article = get_object_or_404(Article, pk=pk)

    context = {'article': article}
    return render(request, 'article_view.html', context)


def article_create_view(request):
    if request.method == "GET":
        form = ArticleForm()
        return render(request, 'article_create.html', context={
            'form': form
        })
    elif request.method == 'POST':
        form = ArticleForm(data=request.POST)
        if form.is_valid():
            # article = Article.objects.create(**form.cleaned_data)
            article = Article.objects.create(
                title=form.cleaned_data['title'],
                text=form.cleaned_data['text'],
                author=form.cleaned_data['author'],
                status=form.cleaned_data['status'],
                publish_at=form.cleaned_data['publish_at']
            )
            return redirect('article_view', pk=article.pk)
        else:
            return render(request, 'article_create.html', context={
                'form': form
            })
    else:
        return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])


def article_update_view(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == "GET":
        form = ArticleForm(initial={
            'title': article.title,
            'text': article.text,
            'author': article.author,
            'status': article.status,
            # форматирование перед выводом для DateTime.
            'publish_at': make_naive(article.publish_at)\
                .strftime(BROWSER_DATETIME_FORMAT)
            # для дат выглядит просто как:
            # 'publish_at': article.publish_at
        })
        return render(request, 'article_update.html', context={
            'form': form,
            'article': article
        })
    elif request.method == 'POST':
        form = ArticleForm(data=request.POST)
        if form.is_valid():
            # Article.objects.filter(pk=pk).update(**form.cleaned_data)
            article.title = form.cleaned_data['title']
            article.text = form.cleaned_data['text']
            article.author = form.cleaned_data['author']
            article.status = form.cleaned_data['status']
            article.publish_at = form.cleaned_data['publish_at']
            article.save()
            return redirect('article_view', pk=article.pk)
        else:
            return render(request, 'article_update.html', context={
                'article': article,
                'form': form
            })
    else:
        return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])


def article_delete_view(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'GET':
        return render(request, 'article_delete.html', context={'article': article})
    elif request.method == 'POST':
        article.delete()
        return redirect('index')
    else:
        return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])
