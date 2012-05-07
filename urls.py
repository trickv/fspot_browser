from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^render/(?P<photo_id>\d+)/$', 'render.views.raw'),
    url(r'^render/(?P<photo_id>\d+)/thumbnail/$', 'render.views.thumbnail'),
    url(r'^render/(?P<photo_id>\d+)/scale/(?P<request_width>\d+)/$', 'render.views.scale'),
    url(r'^$', 'browser.views.tag_list'),
    url(r'^tag/(?P<tag_id>\d+)/$', 'browser.views.tag'),
    url(r'^photo/(?P<photo_id>\d+)/$', 'browser.views.photo'),
    url(r'^time/$', 'browser.views.time'),
    url(r'^time/month/(?P<year_int>\d+)-(?P<month_int>\d+)/$', 'browser.views.month'),
    url(r'^hack/tag-best-2011/(?P<photo_id>\d+)/', 'browser.views.hack_best_2011'),
    url(r'^hack/add_tag/(?P<photo_id>\d+)/(?P<tag_id>\d+)/$', 'browser.views.hack_add_tag'),
    url(r'^hack/remove_tag/(?P<photo_id>\d+)/(?P<tag_id>\d+)/$', 'browser.views.hack_remove_tag'),
    url(r'^hack/remove-best-tag/(?P<photo_id>\d+)/$', 'browser.views.hack_remove_best'),
    # Examples:
    # url(r'^$', 'fspot_browser.views.home', name='home'),
    # url(r'^fspot_browser/', include('fspot_browser.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
