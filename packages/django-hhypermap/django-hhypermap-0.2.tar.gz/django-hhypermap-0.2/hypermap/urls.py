from django.conf.urls import patterns, include, url
from django.conf import settings
from hypermap.proxymap.views import layer_mapproxy, layer_tms

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^layer/(?P<layer_id>\d+)/map(?P<path_info>/.*)$', layer_mapproxy, name='layer_mapproxy'),
    url(r'^layer/(?P<layer_id>\d+)/tms/(?P<z>\d+)/(?P<y>\d+)/(?P<x>\d+).png$', layer_tms, name='layer_tms'),
    url(r'^layer/(?P<layer_id>\d+)/map/config$', layer_tms, name='layer_tms'),
    (r'^', include('hypermap.aggregator.urls')),
    (r'^', include('hypermap.search.urls')),
)

urlpatterns += patterns(
    '',
    url(r'^media/(?P<path>.*)$',
        'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT, }),
)
