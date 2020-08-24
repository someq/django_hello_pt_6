from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseNotAllowed
from django.urls import reverse, reverse_lazy
from django.utils.timezone import make_naive
from django.views.generic import DetailView, CreateView, UpdateView

from webapp.models import Article
from webapp.forms import ArticleForm, BROWSER_DATETIME_FORMAT
from .base_views import SearchView, DeleteView


class IndexView(SearchView):
    template_name = 'article/index.html'
    context_object_name = 'articles'
    paginate_by = 2
    paginate_orphans = 0
    model = Article
    ordering = ['-created_at']
    search_fields = ['title__icontains', 'author__icontains']

    def get_queryset(self):
        data = super().get_queryset()
        if not self.request.GET.get('is_admin', None):
            data = data.filter(status='moderated')
        return data


def article_mass_action_view(request):
    if request.method == 'POST':
        ids = request.POST.getlist('selected_articles', [])
        if 'delete' in request.POST:
            Article.objects.filter(id__in=ids).delete()
    return redirect('index')


class ArticleView(DetailView):
    template_name = 'article/article_view.html'
    model = Article
    paginate_comments_by = 2
    paginate_comments_orphans = 0

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        comments, page, is_paginated = self.paginate_comments(self.object)
        context['comments'] = comments
        context['page_obj'] = page
        context['is_paginated'] = is_paginated

        return context

    def paginate_comments(self, article):
        comments = article.comments.all().order_by('-created_at')
        if comments.count() > 0:
            paginator = Paginator(comments, self.paginate_comments_by, orphans=self.paginate_comments_orphans)
            page_number = self.request.GET.get('page', 1)
            page = paginator.get_page(page_number)
            is_paginated = paginator.num_pages > 1  # page.has_other_pages()
            return page.object_list, page, is_paginated
        else:
            return comments, None, False


class ArticleCreateView(CreateView):
    template_name = 'article/article_create.html'
    form_class = ArticleForm
    model = Article

    def get_success_url(self):
        return reverse('article_view', kwargs={'pk': self.object.pk})


class ArticleUpdateView(UpdateView):
    template_name = 'article/article_update.html'
    form_class = ArticleForm
    model = Article

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs['initial'] = {'publish_at': make_naive(self.object.publish_at)\
    #         .strftime(BROWSER_DATETIME_FORMAT)}
    #     return kwargs

    def get_initial(self):
        return {'publish_at': make_naive(self.object.publish_at)\
            .strftime(BROWSER_DATETIME_FORMAT)}

    def get_success_url(self):
        return reverse('article_view', kwargs={'pk': self.object.pk})


class ArticleDeleteView(DeleteView):
    template_name = 'article/article_delete.html'
    model = Article
    redirect_url = reverse_lazy('index')
    context_key = 'article'
