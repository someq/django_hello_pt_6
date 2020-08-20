from django.shortcuts import get_object_or_404, redirect

from .base_views import CreateView
from webapp.models import Comment, Article
from webapp.forms import ArticleCommentForm


class ArticleCommentCreateView(CreateView):
    model = Comment
    template_name = 'comment/comment_create.html'
    form_class = ArticleCommentForm

    def form_valid(self, form):
        article = get_object_or_404(Article, pk=self.kwargs.get('pk'))
        comment = form.save(commit=False)
        comment.article = article
        comment.save()
        return redirect('article_view', pk=article.pk)

    # def form_valid(self, form):
    #     article = get_object_or_404(Article, pk=self.kwargs.get('pk'))
    #     form.instance.article = article
    #     return super().form_valid(form)
