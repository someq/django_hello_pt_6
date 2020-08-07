from django.contrib import admin
from webapp.models import Article, Comment, Tag, ArticleTag


class ArticleAdmin(admin.ModelAdmin):
    pass


admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment)
admin.site.register(Tag)
admin.site.register(ArticleTag)
