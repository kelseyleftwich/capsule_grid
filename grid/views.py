from django.shortcuts import render, redirect
from grid.models import Article, Plan, Outfit, Profile
from grid.forms import ArticleForm, PlanForm, OutfitForm
from django.http import Http404
from django.contrib.auth.decorators import login_required
import random


def about(request):
	return render(request, 'about.html',)

@login_required
def index(request, article_type=None, weather_type=None):
	if request.user.is_authenticated():
		if article_type:
			articles = Article.objects.filter(article_type=article_type.upper(), user=request.user)
		else:
			articles = Article.objects.filter(user=request.user).order_by('article_type')
		if weather_type:
			articles = articles.filter(weather_type=weather_type.upper()) | articles.filter(weather_type='B')
		return render(
			request,
			'index.html',
			{'articles': articles,}
			)
	else:
		return redirect('registration_register')

@login_required
def plan(request, season_type=None):
	if Plan.objects.filter(user=request.user).count() > 0:
		if season_type:
			plans = Plan.objects.filter(user=request.user, season_type=season_type.upper())
		else:
			plans = Plan.objects.filter(user=request.user)
	else:
		plans = None
	return render(
		request,
		'plan.html',{
			'plans': plans,
		}
		)

@login_required
def plan_detail(request, plan_id):
	plan = Plan.objects.get(id=plan_id)
	if plan.user != request.user:
		raise Http404
	return render(
		request,
		'plans/plan_detail.html',{
			'plan_id': plan_id,
			'plan': plan,
		}
		)

@login_required
def edit_plan(request, plan_id):
	# get object
	plan = Plan.objects.get(id=plan_id)
	# check for valid user
	if plan.user != request.user:
		raise Http404
	form_class = PlanForm
	if request.method == 'POST':
	# grab the data from the form
		form = form_class(data=request.POST, instance=plan, user=request.user)
		if form.is_valid():
			# save the new data
			form.save()
			return render(
				request,
				'plans/plan_detail.html',{
					'plan_id': plan.id,
					'plan': plan,
				}
				)
	# otherwise create the form
	else:
		profile = Profile.objects.get(user=request.user)
		if profile.profile_type == 'P':
			articles = Article.objects.filter(user=request.user).values_list('id','image')
		else:
			articles = Article.objects.filter(user=request.user).values_list('id','image_external')
		form = form_class(instance=plan, user=request.user)
		return render(request, 'plans/edit_plan.html', {'plan': plan, 'form': form, 'articles': articles,})


@login_required
def new_plan(request):
	profile = Profile.objects.get(user=request.user)
	if profile.profile_type == 'P':
		articles = Article.objects.filter(user=request.user).values_list('id','image')
	else:
		articles = Article.objects.filter(user=request.user).values_list('id','image_external')
	
	if request.method == 'POST':
		form = PlanForm(data=request.POST, user=request.user)
		if form.is_valid():
			plan = form.save(commit=False)
			plan.user = request.user
			plan.save()
			cleaned_data = form.clean()
			plan.articles = cleaned_data.get('articles')
			plan.save()
			return render(request,'plans/plan_detail.html',{'plan_id': plan.id,'plan': plan,})
		else:
			return render(request, 'plans/new.html', {'form': form, 'articles': articles,'errors': form.errors,})
	else:
		form = PlanForm(user=request.user)
		return render(request, 'plans/new.html', {'form': form, 'articles': articles,})

@login_required
def outfit(request):
	outfits = Outfit.objects.filter(user=request.user)
	return render(
		request,
		'outfits/outfit.html',
		{'outfits': outfits,}
		)

@login_required
def outfit_detail(request, outfit_id):
	outfit = Outfit.objects.get(id=outfit_id)
	return render(
		request,
		'outfits/outfit_detail.html',
		{'outfit': outfit,}
		)

@login_required
def new_outfit(request):
	if request.method == 'POST':
		form = OutfitForm(data=request.POST, user=request.user)
		if form.is_valid():
			outfit = form.save(commit=False)
			outfit.user = request.user
			outfit.save()
			# get clean form data and add articles to saved object
			cleaned_data = form.clean()
			outfit.articles = cleaned_data.get('articles')
			outfit.save()
			return redirect('outfit')
		return render(request, 'outfits/new.html', {'form': form,})

	else:
		profile = Profile.objects.get(user=request.user)
		if profile.profile_type == 'P':
			articles = Article.objects.filter(user=request.user).values_list('id','image')
		else:
			articles = Article.objects.filter(user=request.user).values_list('id','image_external')
		form = OutfitForm(user=request.user)
		return render(request, 'outfits/new.html', {'form': form, 'articles':articles})

@login_required
def outfit_random_save(request):
	if request.method=='POST':
		outfit = Outfit()
		outfit.name = request.POST['outfit_name']
		outfit.user = request.user
		outfit.save()
		if 'top_id' in request.POST:
			top = Article.objects.get(id=request.POST['top_id'])
			outfit.articles.add(top)
		if 'bottom_id' in request.POST:
			bottom = Article.objects.get(id=request.POST['bottom_id'])
			outfit.articles.add(bottom)
		if 'outer_id' in request.POST:
			outer = Article.objects.get(id=request.POST['outer_id'])
			outfit.articles.add(outer)
		if 'detail_id' in request.POST:
			detail = Article.objects.get(id=request.POST['detail_id'])
			outfit.articles.add(detail)
		if 'shoes_id' in request.POST:
			shoes = Article.objects.get(id=request.POST['shoes_id'])
			outfit.articles.add(shoes)
		if 'dress_id' in request.POST:
			dress = Article.objects.get(id=request.POST['dress_id'])
			outfit.articles.add(dress)
		outfit.save()
	return redirect('outfit')

@login_required
def edit_outfit(request, outfit_id):
	# get object
	outfit = Outfit.objects.get(id=outfit_id)
	# check user
	if outfit.user != request.user:
		raise Http404
	form_class = OutfitForm
	if request.method == 'POST':
		form = form_class(data=request.POST, instance=outfit, user=request.user)
		if form.is_valid():
			form.save()
			return redirect('outfit')
	else:
		articles = Article.objects.filter(user=request.user).values_list('id','image')
		form = form_class(instance=outfit, user=request.user)
		return render(request, 'outfits/edit_outfit.html', {'outfit': outfit, 'form': form,'articles':articles})

@login_required
def outfit_random(request, plan_id=None):
	plans = Plan.objects.filter(user=request.user)

	if plan_id:
		plan = Plan.objects.get(id=plan_id)
		if plan.user != request.user:
			raise Http404
		articles = plan.articles

	else:
		articles = Article.objects.filter(user=request.user).order_by('?')
		plan=None

	outer = articles.filter(article_type='O').order_by('?').first()
	detail = articles.filter(article_type='A').order_by('?').first()
	shoes = articles.filter(article_type='S').order_by('?').first()

	if (articles.filter(article_type='T').count() == 0 or articles.filter(article_type='B').count() == 0) and articles.filter(article_type='D').count() == 0:
		message = "Not enough articles to generate an outfit. Random outfit generator looks for a top and bottom article or dress as the outfit base. "
	else:
		message = None

	# if no tops - pick dress
	if articles.filter(article_type='T').count() == 0:
		dress = articles.filter(article_type='D').order_by('?').first()
		print("dress")
		return render(
			request,
			'outfits/outfit_random.html',
			{
			'dress': dress,
			'outer': outer,
			'detail': detail,
			'shoes': shoes,
			'plans': plans,
			'plan':plan,
			'message': message,
			})
	# if no bottoms - pick dress
	elif articles.filter(article_type='B').count() == 0:
		dress = articles.filter(article_type='D').order_by('?').first()
		print("dress 2")
		return render(
			request,
			'outfits/outfit_random.html',
			{
			'dress': dress,
			'outer': outer,
			'detail': detail,
			'shoes': shoes,
			'plans':plans,
			'plan':plan,
			'message': message,

			})
	# randomly pick dress or top + bottom combo
	else:
		flip = random.randint(0, 1)
		if(flip == 0 and (articles.filter(article_type='D').count() != 0)):
			dress = articles.filter(article_type='D').order_by('?').first()
			print("Dress 3")
			return render(
				request,
				'outfits/outfit_random.html',
				{
				'dress': dress,
				'outer': outer,
				'detail': detail,
				'shoes': shoes,
				'plans':plans,
				'plan':plan,
				'message': message,

				})
		else:
			top = articles.filter(article_type='T').order_by('?').first()
			bottom = articles.filter(article_type='B').order_by('?').first()
			print("top and bottom")
			return render(
				request,
				'outfits/outfit_random.html',
				{
				'top': top,
				'bottom': bottom,
				'outer': outer,
				'detail': detail,
				'shoes': shoes,
				'plans':plans,
				'plan':plan,
				'message': message,

				})


@login_required
def article_detail(request, article_id):
	article = Article.objects.get(id=article_id)
	return render(
		request,
		'articles/article_detail.html',
		{'article': article,}
		)

@login_required
def browse_by_name(request, initial=None):
	if initial:
		articles = Article.objects.filter(name__istartswith=initial, user=request.user).order_by('name')
		#articles = Article.objects.filter(name__istartswith=initial).order_by('name')
	else:
		articles = Article.objects.filter(user=request.user).order_by('name')
		#articles = Article.objects.all().order_by('name')
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
			return render(request, 'articles/new.html', {'form': form, 'errors':form.errors,})
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

@login_required
def delete_outfit(request, outfit_id):
	# grab the object
	outfit = Outfit.objects.get(id=outfit_id)
	# check for valid user
	if outfit.user != request.user:
		raise Http404
	# if the form has been submitted
	if request.method == 'POST':
		# grab the data from the form
		outfit.delete()
		return render(request, 'outfits/delete_outfit.html', {'outfit': outfit, 'message': "success"})
	# otherwise create the form
	else:
		return render(request, 'outfits/delete_outfit.html', {'outfit': outfit,})

@login_required
def delete_plan(request, plan_id):
	# grab the object
	plan = Plan.objects.get(id=plan_id)
	# check for valid user
	if plan.user != request.user:
		raise Http404
	# if the form has been submitted
	if request.method == 'POST':
		# grab the data from the form
		plan.delete()
		return render(request, 'plans/delete_plan.html', {'plan': plan, 'message': "success"})
	# otherwise create the form
	else:
		return render(request, 'plans/delete_plan.html', {'plan': plan,})