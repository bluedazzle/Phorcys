from django.conf.urls import patterns, include, url
from django.contrib import admin

from Phorcys import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'Phorcys.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^site_admin/', include(admin.site.urls)),
    url(r'^admin/', include('myadmin.urls')),
    url(r'^', include('core.urls')),
    url(r'^api/v1/user/', include('myuser.urls')),
    url(r'^api/v1/lol/', include('lol.urls')),
    url(r'^s/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_MEDIA}),
)
