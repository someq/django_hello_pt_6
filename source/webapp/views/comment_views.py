from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, DeleteView

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
        # form.save_m2m()  ## для сохранения связей многие-ко-многим
        return redirect('article_view', pk=article.pk)

    # def form_valid(self, form):
    #     article = get_object_or_404(Article, pk=self.kwargs.get('pk'))
    #     form.instance.article = article
    #     return super().form_valid(form)


class CommentUpdateView(UpdateView):
    model = Comment
    template_name = 'comment/comment_update.html'
    form_class = ArticleCommentForm

    def get_success_url(self):
        return reverse('article_view', kwargs={'pk': self.object.article.pk})


class CommentDeleteView(DeleteView):
    model = Comment

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('article_view', kwargs={'pk': self.object.article.pk})
