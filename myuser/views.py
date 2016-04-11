# coding: utf-8

from __future__ import unicode_literals

import json
import random
import string

import datetime
from django.utils.timezone import get_current_timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from core.Mixin.CheckMixin import CheckSecurityMixin, CheckTokenMixin
from core.Mixin.StatusWrapMixin import *
from core.dss.Mixin import MultipleJsonResponseMixin, FormJsonResponseMixin, JsonResponseMixin
from django.shortcuts import render

# Create your views here.
from myuser.forms import VerifyCodeForm, UserRegisterForm
from myuser.models import EUser, Verify


class VerifyCodeView(CheckSecurityMixin, StatusWrapMixin, JsonResponseMixin, CreateView):
    form_class = VerifyCodeForm
    http_method_names = ['post', 'get']
    success_url = 'localhost'
    count = 6

    def get(self, request, *args, **kwargs):
        phone = request.GET.get('phone')
        code = request.GET.get('code')
        if phone and code:
            verify_list = Verify.objects.filter(phone=unicode(phone)).order_by('-create_time')
            if verify_list.exists():
                verify = verify_list[0]
                now_time = datetime.datetime.now(tz=get_current_timezone())
                if now_time - verify.create_time > datetime.timedelta(minutes=30):
                    self.status_code = INFO_EXPIRE
                    self.message = '验证码已过期, 请重新获取'
                    verify.delete()
                    return self.render_to_response(dict())
                if verify.code != unicode(code):
                    self.status_code = ERROR_VERIFY
                    self.message = '验证码不正确'
                    return self.render_to_response(dict())
                verify.delete()
                return self.render_to_response(dict())
            else:
                self.status_code = INFO_NO_VERIFY
                self.message = '请获取验证码'
                return self.render_to_response(dict())
        self.status_code = ERROR_DATA
        self.message = '数据缺失'
        return self.render_to_response(dict())

    def form_valid(self, form):
        super(VerifyCodeView, self).form_valid(form)
        self.object.code = self.create_verify_code()
        self.object.save()
        return self.render_to_response(dict())

    def form_invalid(self, form):
        super(VerifyCodeView, self).form_invalid(form)
        self.status_code = ERROR_DATA
        print form.errors.as_json()
        self.message = json.loads(form.errors.as_json()).get('phone')[0].get('message')
        return self.render_to_response(dict())

    def create_verify_code(self):
        return string.join(
            random.sample('1234567890', self.count)).replace(" ", "")


class UserRegisterView(CheckSecurityMixin, StatusWrapMixin, JsonResponseMixin, CreateView):
    form_class = UserRegisterForm
    http_method_names = ['post']
    success_url = 'localhost'
    datetime_type = 'timestamp'
    include_attr = ['token', 'id', 'create_time', 'nick', 'phone']
    count = 64
    token = ''

    def form_valid(self, form):
        super(UserRegisterView, self).form_valid(form)
        self.token = self.create_token()
        self.object.token = self.token
        self.object.set_password(form.cleaned_data.get('password'))
        self.object.save()
        return self.render_to_response(self.object)

    def form_invalid(self, form):
        super(UserRegisterView, self).form_invalid(form)
        self.status_code = ERROR_DATA
        self.message = json.loads(form.errors.as_json()).values()[0][0].get('message')
        return self.render_to_response(dict())

    def create_token(self):
        return string.join(
            random.sample('ZYXWVUTSRQPONMLKJIHGFEDCBA1234567890zyxwvutsrqponmlkjihgfedcbazyxwvutsrqponmlkjihgfedcba',
                          self.count)).replace(" ", "")


class UserResetView(CheckSecurityMixin, StatusWrapMixin, JsonResponseMixin, UpdateView):
    # form_class =
    pass

