from django.conf.urls import patterns, include, url
from myuser.views import *

urlpatterns = patterns('',
                       url(r'^verify', VerifyCodeView.as_view()),
                       url(r'^register', UserRegisterView.as_view()),
                       )
