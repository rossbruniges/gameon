from django.conf.urls.defaults import patterns, url

from . import views

urlpatterns = patterns('',
    url(r'^apply/$', views.create, name='submissions.create_entry'),
    url(r'^entries/all/$', views.list, name='submissions.entry_list'),
    url(r'^entries/(?P<slug>[\w-]+)/$', views.single,
        name='submissions.entry_single'),
    # category views
    # edit entry
)
