from django.shortcuts import render, redirect
from grid.models import Article, Plan
from grid.forms import ArticleForm, PlanForm
from django.http import Http404
from django.contrib.auth.decorators import login_required
import random


def index(request, article_type=None):
	if article_type:
		articles = Article.objects.filter(article_type=article_type.upper(), user=request.user)
	else:
		articles = Article.objects.filter(user=request.user).order_by('article_type')
	return render(
		request,
		'index.html',
		{'articles': articles,}
		)

def plan(request):
	if Plan.objects.filter(user=request.user).count() > 0:
		plan = Plan.objects.get(user=request.user)
	else:
		plan = None
	tops_actual = Article.objects.filter(article_type='T', user=request.user).count()
	bottoms_actual = Article.objects.filter(article_type='B', user=request.user).count()
	dresses_actual = Article.objects.filter(article_type='D', user=request.user).count()
	details_actual = Article.objects.filter(article_type='A', user=request.user).count()
	shoes_actual = Article.objects.filter(article_type='S', user=request.user).count()
	outer_actual = Article.objects.filter(article_type='O', user=request.user).count()
	total_actual = Article.objects.filter(user=request.user).count()
	return render(
		request,
		'plan.html',{
			'plan': plan,
			'tops_actual': tops_actual,
			'bottoms_actual': bottoms_actual,
			'dresses_actual': dresses_actual,
			'details_actual': details_actual,
			'shoes_actual': shoes_actual,
			'outer_actual': outer_actual,
			'total_actual': total_actual,
		}
		)

@login_required
def new_plan(request):
	# get object if one exists
	if Plan.objects.filter(user=request.user).count() > 0:
			plan = Plan.objects.get(user=request.user)
			# check for valid user
			if plan.user != request.user:
				raise Http404
			# set the form we're using...
			form_class = PlanForm
			# if the form has been submitted
			if request.method == 'POST':
			# grab the data from the form
				form = form_class(data=request.POST, instance=plan)
				if form.is_valid():
					# save the new data
					form.save()
					return redirect('plan')
			# otherwise create the form
			else:
				form = form_class(instance=plan)
				return render(request, 'plans/new.html', {'form': form,})
	# object doesn't exist
	else:
		if request.method == 'POST':
			form = PlanForm(data=request.POST)
			if form.is_valid():
				plan = form.save(commit=False)
				plan.user = request.user
				plan.save()
				return redirect('plan')
		else:
			form = PlanForm()
		return render(request, 'plans/new.html', {'form': form,})

def outfit(request):
	outer = Article.objects.filter(article_type='O', user=request.user).order_by('?').first()
	detail = Article.objects.filter(article_type='A', user=request.user).order_by('?').first()
	shoes = Article.objects.filter(article_type='S', user=request.user).order_by('?').first()

	if Article.objects.filter(article_type='T', user=request.user).count() == 0:
		dress = Article.objects.filter(article_type='D', user=request.user).order_by('?').first()
		return render(
			request,
			'outfit.html',
			{
			'dress': dress,
			'outer': outer,
			'detail': detail,
			'shoes': shoes,
			})
	elif Article.objects.filter(article_type='B', user=request.user).count() == 0:
		dress = Article.objects.filter(article_type='D', user=request.user).order_by('?').first()
		return render(
			request,
			'outfit.html',
			{
			'dress': dress,
			'outer': outer,
			'detail': detail,
			'shoes': shoes,
			})
	else:
		flip = random.randint(0, 1)
		if(flip == 0 and Article.objects.filter(article_type='D', user=request.user).count() != 0):
			dress = Article.objects.filter(article_type='D', user=request.user).order_by('?').first()
			return render(
				request,
				'outfit.html',
				{
				'dress': dress,
				'outer': outer,
				'detail': detail,
				'shoes': shoes,
				})
		else:
			top = Article.objects.filter(article_type='T', user=request.user).order_by('?').first()
			bottom = Article.objects.filter(article_type='B', user=request.user).order_by('?').first()
			return render(
				request,
				'outfit.html',
				{
				'top': top,
				'bottom': bottom,
				'outer': outer,
				'detail': detail,
				'shoes': shoes,
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

@login_required
def delete_article(request, article_id):
	# grab the object
	article = Article.objects.get(id=article_id)
	# check for valid user
	if article.user != request.user:
		raise Http404
	# if the form has been submitted
	if request.method == 'POST':
		# grab the data from the form
		article.delete()
		return render(request, 'articles/delete_article.html', {'article': article, 'message': "success"})
	# otherwise create the form
	else:
		return render(request, 'articles/delete_article.html', {'article': article,})