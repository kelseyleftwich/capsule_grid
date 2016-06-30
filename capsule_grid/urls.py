"""capsule_grid URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from grid import views
from capsule_grid import settings
from django.views.generic import TemplateView, RedirectView
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
	url(r'^$', views.index, name='home'),
	url(r'^browse/type/(?P<article_type>[-\w]+)/$', views.index, name='article_type'),
	# object detail
	url(r'^articles/(?P<article_id>[0-9]+)/$', views.article_detail, name='article_detail'),
	# object edit
	url(r'^articles/(?P<article_id>[-\w]+)/edit/$', views.edit_article, name='edit_article'),
	# object delete
	url(r'^articles/(?P<article_id>[-\w]+)/delete/$', views.delete_article, name='delete_article'),
	# object new
	url(r'^articles/new/$', views.new_article, name='new_article'),
	# object new
	url(r'^plan/new/$', views.new_plan, name='new_plan'),
	# outfit
	url(r'^outfit/$', views.outfit, name='outfit'),
	# plan
	url(r'^plan/$', views.plan, name='plan'),
	# object browse
    url(r'^browse/$', RedirectView.as_view(pattern_name='browse', permanent=True)),
	url(r'^browse/name/$',
	        views.browse_by_name, name='browse'),
	url(r'^browse/name/(?P<initial>[-\w]+)/$',
        views.browse_by_name, name='browse_by_name'),
	#registration
	url(r'^accounts/', include('registration.backends.simple.urls')),
	#admin
    url(r'^admin/', admin.site.urls),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
