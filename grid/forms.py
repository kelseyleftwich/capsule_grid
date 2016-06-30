from django.forms import ModelForm
from django import forms
from grid.models import Article, Plan

class ArticleForm(ModelForm):
	class Meta:
		model = Article
		fields = ('name', 'description', 'image', 'article_type')
		file = forms.ImageField()

class PlanForm(ModelForm):
	class Meta:
		model = Plan
		fields = ('top_count', 'bottom_count', 'dress_count','shoe_count','details_count','outer_count')