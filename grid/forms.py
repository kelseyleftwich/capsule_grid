from django.forms import ModelForm
from django import forms
from django.utils.safestring import mark_safe
from grid.models import Article, Plan, Outfit

class ArticleForm(ModelForm):
	class Meta:
		model = Article
		fields = ('name', 'description', 'image', 'article_type')
		file = forms.ImageField()

class PlanForm(ModelForm):
	class Meta:
		model = Plan
		fields = (
			'name',
			'top_count',
			'bottom_count',
			'dress_count',
			'shoe_count',
			'details_count',
			'outer_count',
			'season_type'
			)

class OutfitForm(ModelForm):
	class Meta:
		model = Outfit
		fields = ('name','articles')
