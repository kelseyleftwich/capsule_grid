from django.forms import ModelForm
from django import forms
from django.utils.safestring import mark_safe
from grid.models import Article, Plan, Outfit
from django.forms.widgets import CheckboxSelectMultiple

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
	def __init__(self, *args, **kwargs):
		super(OutfitForm, self).__init__(*args, **kwargs)
		articles = Article.objects.all()
		items = []
		for article in articles:
		    items.append((article.pk, mark_safe('%s' % article.image.url)))
		self.fields['articles'].widget = CheckboxSelectMultiple()
		self.fields['articles'].choices = items