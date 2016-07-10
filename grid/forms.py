from django.forms import ModelForm
from django import forms
from grid.models import Article, Plan, Outfit

class ArticleForm(ModelForm):
	class Meta:
		model = Article
		fields = (
			'name',
			'description', 
			'image', 
			'article_type', 
			'weather_type', 
			'image_external', 
			'image_slurp',
			)
		file = forms.ImageField()


CASE_SQL = '(case when article_type="T" then 1 when article_type="B" then 2 when article_type="O" then 3 when article_type="D" then 4 when article_type="A" then 5 when article_type="S" then 6 end)'

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
			'season_type',
			'articles',
			'public',
			)

	def __init__(self, user, *args, **kwargs):
		super(PlanForm, self).__init__(*args, **kwargs)
		self.fields['articles'] = forms.ModelMultipleChoiceField(
			queryset = Article.objects.filter(user=user).extra(select={'article_order': CASE_SQL}, order_by=['article_order']),
			widget=forms.CheckboxSelectMultiple,
			required=False
			)
		self.fields['public'] = forms.BooleanField(widget=forms.Select(choices=((False, 'No'), (True, 'Yes'))))


class OutfitForm(ModelForm):
	class Meta:
		model = Outfit
		fields = ('name','articles')



	def __init__(self, user, *args, **kwargs):
		super(OutfitForm, self).__init__(*args, **kwargs)
		self.fields['articles'] = forms.ModelMultipleChoiceField(
			queryset = Article.objects.filter(user=user).extra(select={'article_order': CASE_SQL}, order_by=['article_order']),
			widget=forms.CheckboxSelectMultiple
			)