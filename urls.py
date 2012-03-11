from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^render/(?P<photo_id>\d+)/$', 'render.views.raw'),
    url(r'^render/(?P<photo_id>\d+)/thumbnail/$', 'render.views.thumbnail'),
    url(r'^$', 'browser.views.tag_list'),
    url(r'^tag/(?P<tag_id>\d+)/$', 'browser.views.tag'),
    # Examples:
    # url(r'^$', 'fspot_browser.views.home', name='home'),
    # url(r'^fspot_browser/', include('fspot_browser.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
