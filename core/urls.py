from django.conf.urls import patterns, include, url
from django.contrib import admin
from core.views import check_signs

urlpatterns = patterns('',
                       url(r'^check$', check_signs),
                       )
