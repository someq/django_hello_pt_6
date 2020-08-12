from django.core.validators import MinLengthValidator
from django.db import models
from django.utils import timezone


STATUS_CHOICES = [
    ('new', 'Не модерировано'),
    ('moderated', 'Модерировано'),
    ('rejected', 'Отклонено')
]


class Article(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False, verbose_name='Заголовок',
                             validators=[MinLengthValidator(10)])
    text = models.TextField(max_length=3000, null=False, blank=False, verbose_name='Текст')
    author = models.CharField(max_length=40, null=False, blank=False, default='Unknown', verbose_name='Автор')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='new', verbose_name='Модерация')
    tags = models.ManyToManyField('webapp.Tag', verbose_name='Теги', blank=True, related_name='articles')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    publish_at = models.DateTimeField(verbose_name="Время публикации", blank=True, default=timezone.now)

    def save(self, **kwargs):
        if not self.publish_at:
            if not self.pk:
                self.publish_at = timezone.now()
            else:
                self.publish_at = Article.objects.get(pk=self.pk).publish_at
        super().save(**kwargs)

    def __str__(self):
        return "{}. {}".format(self.pk, self.title)

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


class Comment(models.Model):
    article = models.ForeignKey('webapp.Article', related_name='comments',
                                on_delete=models.CASCADE, verbose_name='Статья')
    text = models.TextField(max_length=400, verbose_name='Комментарий')
    author = models.CharField(max_length=40, null=True, blank=True, default='Аноним', verbose_name='Автор')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Время изменения')

    def __str__(self):
        return self.text[:20]

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class Tag(models.Model):
    name = models.CharField(max_length=31, verbose_name='Тег')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')

    def __str__(self):
        return self.name
