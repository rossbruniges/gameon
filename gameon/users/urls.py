from django.conf.urls.defaults import patterns, url

from . import views

urlpatterns = patterns('',
    url(r'^signout/$', views.signout, name='users_signout'),
    url(r'^profile/edit/$', views.edit, name='users_edit'),
    url(r'^profile/(?P<username>[\w-]+)/$', views.profile,
        name='users_profile'),
)
