from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotAllowed
from django.urls import reverse

from webapp.models import Article, STATUS_CHOICES


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
    article = get_object_or_404(Article, pk=pk)
    context = {'article': article}
    return render(request, 'article_view.html', context)


def article_create_view(request):
    if request.method == "GET":
        return render(request, 'article_create.html', context={
            'status_choices': STATUS_CHOICES
        })
    elif request.method == 'POST':
        title = request.POST.get('title')
        text = request.POST.get('text')
        author = request.POST.get('author')
        status = request.POST.get('status')
        article = Article.objects.create(title=title, text=text, author=author, status=status)

        # redirect_url = reverse('article_view', kwargs={'pk': article.pk})
        return redirect('article_view', pk=article.pk)
    else:
        return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])


def article_update_view(request, pk):
    # article = Article.objects.get(pk=pk)
    article = get_object_or_404(Article, pk=pk)
    if request.method == "GET":
        return render(request, 'article_update.html', context={
            'status_choices': STATUS_CHOICES,
            'article': article
        })
    elif request.method == 'POST':
        errors = {}
        article.title = request.POST.get('title')
        if not article.title:
            errors['title'] = 'This field is required!'
        article.text = request.POST.get('text')
        if not article.text:
            errors['text'] = 'This field is required!'
        article.author = request.POST.get('author')
        if not article.author:
            errors['author'] = 'This field is required!'
        article.status = request.POST.get('status')

        if errors:
            return render(request, 'article_update.html', context={
                'status_choices': STATUS_CHOICES,
                'article': article,
                'errors': errors
            })

        article.save()
        return redirect('article_view', pk=article.pk)
    else:
        return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])

