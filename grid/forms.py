from django.forms import ModelForm
from django import forms
from grid.models import Article, Plan, Outfit

class ArticleForm(ModelForm):
	class Meta:
		model = Article
		fields = ('name', 'description', 'image', 'article_type', 'weather_type', 'image_external')
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


	def __init__(self, user, *args, **kwargs):
		super(OutfitForm, self).__init__(*args, **kwargs)
		self.fields['articles'] = forms.ModelMultipleChoiceField(
			queryset = Article.objects.filter(user=user),
			widget=forms.CheckboxSelectMultiple
			)