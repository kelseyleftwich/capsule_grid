from django.forms import ModelForm
from django import forms
from grid.models import Article

class ArticleForm(ModelForm):
	class Meta:
		model = Article
		fields = ('name', 'description', 'image', 'article_type')
		file = forms.ImageField()