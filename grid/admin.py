from django.contrib import admin
from grid.models import Article, Plan, Outfit

class ArticleAdmin(admin.ModelAdmin):
	model = Article
	list_display = ('name', 'article_type', 'weather_type', 'user')

class PlanAdmin(admin.ModelAdmin):
	model = Plan
	list_display = ('name', 'user')

class OutfitAdmin(admin.ModelAdmin):
	model = Outfit
	list_display = ('__str__', 'user')

admin.site.register(Article, ArticleAdmin)
admin.site.register(Plan, PlanAdmin)
admin.site.register(Outfit, OutfitAdmin)

