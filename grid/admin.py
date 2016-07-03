from django.contrib import admin
from grid.models import Article, Plan, Outfit, Profile

class ArticleAdmin(admin.ModelAdmin):
	model = Article
	list_display = ('name', 'article_type', 'weather_type', 'user')

class PlanAdmin(admin.ModelAdmin):
	model = Plan
	list_display = ('name', 'user')

class OutfitAdmin(admin.ModelAdmin):
	model = Outfit
	list_display = ('__str__', 'user')


class ProfileAdmin(admin.ModelAdmin):
	model = Profile
	list_display = ('user',)


admin.site.register(Article, ArticleAdmin)
admin.site.register(Plan, PlanAdmin)
admin.site.register(Outfit, OutfitAdmin)
admin.site.register(Profile, ProfileAdmin)

