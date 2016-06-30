from django.shortcuts import render, redirect
from grid.models import Article
from grid.forms import ArticleForm
from django.http import Http404
from django.contrib.auth.decorators import login_required


def index(request, article_type=None):
	if article_type:
		articles = Article.objects.filter(article_type=article_type.upper())
	else:
		articles = Article.objects.all().order_by('article_type')
	return render(
		request,
		'index.html',
		{'articles': articles,}
		)

def outfit(request):
	top = Article.objects.filter(article_type='T').order_by('?').first()
	bottom = Article.objects.filter(article_type='B').order_by('?').first()
	outer = Article.objects.filter(article_type='O').order_by('?').first()
	detail = Article.objects.filter(article_type='A').order_by('?').first()
	return render(
		request,
		'outfit.html',
		{
		'top': top,
		'bottom': bottom,
		'outer': outer,
		'detail': detail,
		})


def article_detail(request, article_id):
	article = Article.objects.get(id=article_id)
	return render(
		request,
		'articles/article_detail.html',
		{'article': article,}
		)

def browse_by_name(request, initial=None):
	if initial:
		#articles = Article.objects.filter(name__istartswith=initial, user=request.user).order_by('name')
		articles = Article.objects.filter(name__istartswith=initial).order_by('name')
	else:
		#articles = Article.objects.filter(user=request.user).order_by('name')
		articles = Article.objects.all().order_by('name')
	return render(request, 'search/search.html', {
		'articles': articles,
		'initial': initial,
	})

@login_required
def new_article(request):
	if request.method == 'POST':
		form = ArticleForm(data=request.POST, files=request.FILES)
		if form.is_valid():
			article = form.save(commit=False)
			article.user = request.user
			article.save()
			return redirect('article_detail', article_id = article.id)
	else:
		form = ArticleForm()
	return render(request, 'articles/new.html', {'form': form,})

@login_required
def edit_article(request, article_id):
	# grab the object
	article = Article.objects.get(id=article_id)
	# check for valid user
	if article.user != request.user:
		raise Http404
	# set the form we're using...
	form_class = ArticleForm
	# if the form has been submitted
	if request.method == 'POST':
		# grab the data from the form
		form = form_class(data=request.POST, instance=article, files=request.FILES)
		if form.is_valid():
			# save the new data
			form.save()
			return redirect('article_detail', article_id = article.id)
	# otherwise create the form
	else:
		form = form_class(instance=article)
		return render(request, 'articles/edit_article.html', {'article': article, 'form': form,})

