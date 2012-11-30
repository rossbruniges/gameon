from django.conf.urls.defaults import *

from . import views


urlpatterns = patterns('',
    url(r'^$', views.home, name='static_site.home'),
    url(r'^rules/$', views.rules, name='static_site.rules'),
    url(r'^judges/$', views.judges, name='static_site.judges'),
    url(r'^faqs/$', views.faqs, name='static_site.faqs'),
    url(r'^judging/$', views.judging, name='static_site.judging'),
    url(r'^prizes/$', views.prizes, name='static_site.prizes'),
    url(r'^resources/$', views.resources, name='static_site.resources'),
    url(r'^legal/rules/$', views.legal, name='static_site.legal'),
)
