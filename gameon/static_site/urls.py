from django.conf.urls.defaults import *

from . import views


urlpatterns = patterns('',
    url(r'^$', views.home, name='static_site.home'),
    url(r'^rules/$', views.rules, name='static_site.rules'),
    url(r'^judges/$', views.judges, name='static_site.judges'),
    url(r'^prizes/$', views.prizes, name='static_site.prizes'),
    url(r'^resources/$', views.resources, name='static_site.resources'),
    url(r'^previous/$', views.previous, name='static_site.previous'),
    url(r'^categories/$', views.categories, name='static_site.categories'),
    url(r'^legal/rules/$', views.legal, name='static_site.legal'),
)
