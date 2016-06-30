from django.contrib import admin
from grid.models import Article, Plan

class ArticleAdmin(admin.ModelAdmin):
	model = Article
	list_display = ('name', 'description', 'user')

class PlanAdmin(admin.ModelAdmin):
	model = Plan
	list_display = ('top_count', 'bottom_count', 'dress_count','shoe_count','details_count','outer_count')

admin.site.register(Article, ArticleAdmin)
admin.site.register(Plan, PlanAdmin)
