from django.contrib import admin
from grid.models import Article

class ArticleAdmin(admin.ModelAdmin):
	model = Article
	list_display = ('name', 'description', 'user')

admin.site.register(Article, ArticleAdmin)