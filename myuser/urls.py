from django.conf.urls import patterns, include, url
from myuser.views import *

urlpatterns = patterns('',
                       url(r'^verify', VerifyCodeView.as_view()),
                       url(r'^register', UserRegisterView.as_view()),
                       url(r'^password/forget', UserResetView.as_view()),
                       url(r'^password/change', UserChangePasswordView.as_view()),
                       url(r'^login', UserLoginView.as_view()),
                       url(r'^logout', UserLogoutView.as_view()),
                       )
