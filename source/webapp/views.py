from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotAllowed
from django.urls import reverse
from django.utils.timezone import make_naive
from django.views.generic import ListView, TemplateView, FormView

from webapp.models import Article
from .forms import ArticleForm, BROWSER_DATETIME_FORMAT, SimpleSearchForm
from .base_views import FormView as CustomFormView, ListView as CustomListView


class IndexView(ListView):
    template_name = 'index.html'
    context_object_name = 'articles'
    paginate_by = 2
    paginate_orphans = 0

    def get_context_data(self, *, object_list=None, **kwargs):
        form = SimpleSearchForm(data=self.request.GET)
        if form.is_valid():
            search = form.cleaned_data['search']
            kwargs['search'] = search
        return super().get_context_data(object_list=object_list, **kwargs)

    def get_queryset(self):
        data = Article.objects.all()

        if not self.request.GET.get('is_admin', None):
            data = Article.objects.filter(status='moderated')

        # http://localhost:8000/?search=ygjkjhg
        form = SimpleSearchForm(data=self.request.GET)
        if form.is_valid():
            search = form.cleaned_data['search']
            if search:
                data = data.filter(Q(title__icontains=search) | Q(author__icontains=search))

        return data.order_by('-created_at')


class ArticleView(TemplateView):
    template_name = 'article_view.html'
    paginate_comments_by = 2
    paginate_comments_orphans = 0

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        pk = self.kwargs.get('pk')
        article = get_object_or_404(Article, pk=pk)

        comments = article.comments.all().order_by('-created_at')
        if comments.count() > 0:
            paginator = Paginator(comments, self.paginate_comments_by, orphans=self.paginate_comments_orphans)
            page_number = self.request.GET.get('page', 1)
            page = paginator.get_page(page_number)

            context['page_obj'] = page
            context['is_paginated'] = paginator.num_pages > 1  # page.has_other_pages()
            context['comments'] = page.object_list
        else:
            context['is_paginated'] = False
            context['comments'] = comments

        context['article'] = article
        return context


class ArticleCreateView(CustomFormView):
    template_name = 'article_create.html'
    form_class = ArticleForm

    def form_valid(self, form):
        self.article = form.save()
        return super().form_valid(form)

    def get_redirect_url(self):
        return reverse('article_view', kwargs={'pk': self.article.pk})


class ArticleUpdateView(FormView):
    template_name = 'article_update.html'
    form_class = ArticleForm

    def dispatch(self, request, *args, **kwargs):
        self.article = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['article'] = self.article
        return context

    def get_initial(self):
        return {'publish_at': make_naive(self.article.publish_at)\
            .strftime(BROWSER_DATETIME_FORMAT)}

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.article
        return kwargs

    def form_valid(self, form):
        self.article = form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('article_view', kwargs={'pk': self.article.pk})

    def get_object(self):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Article, pk=pk)


def article_delete_view(request, pk):
    article = get_object_or_404(Article, pk=pk)
    if request.method == 'GET':
        return render(request, 'article_delete.html', context={'article': article})
    elif request.method == 'POST':
        article.delete()
        return redirect('index')
    else:
        return HttpResponseNotAllowed(permitted_methods=['GET', 'POST'])
