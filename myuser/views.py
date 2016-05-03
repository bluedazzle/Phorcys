# coding: utf-8

from __future__ import unicode_literals

import json
import random
import string

import datetime

from django.utils.timezone import get_current_timezone
from django.views.generic import ListView, DetailView, CreateView, UpdateView, View

from core.Mixin.CheckMixin import CheckSecurityMixin, CheckTokenMixin
from core.Mixin.StatusWrapMixin import *
from core.dss.Mixin import MultipleJsonResponseMixin, FormJsonResponseMixin, JsonResponseMixin

# Create your views here.
from core.sms import send_sms
from core.utils import upload_picture, save_image
from lol.models import LOLInfoExtend
from myuser.forms import VerifyCodeForm, UserRegisterForm, UserResetForm, UserLoginForm, UserChangePasswordForm, \
    UserThirdRegisterForm
from myuser.models import EUser, Verify, Invite
import time


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
        verify = self.create_verify_code()
        if send_sms(verify, form.cleaned_data.get('phone')):
            self.object.code = verify
            self.object.save()
            return self.render_to_response(dict())
        self.status_code = ERROR_UNKNOWN
        self.message = '短信发送失败,请重试'
        return self.render_to_response(dict())

    def form_invalid(self, form):
        super(VerifyCodeView, self).form_invalid(form)
        self.status_code = ERROR_DATA
        self.message = json.loads(form.errors.as_json()).values()[0][0].get('message')
        return self.render_to_response(dict())

    def create_verify_code(self):
        return string.join(
            random.sample('1234567890', self.count)).replace(" ", "")


class UserRegisterView(CheckSecurityMixin, StatusWrapMixin, JsonResponseMixin, CreateView):
    form_class = UserRegisterForm
    http_method_names = ['post']
    success_url = 'localhost'
    datetime_type = 'timestamp'
    include_attr = ['token', 'id', 'create_time', 'nick', 'phone', 'avatar']
    count = 64
    token = ''

    def create_extend(self):
        new_lol_extend = LOLInfoExtend()
        new_lol_extend.save()
        self.object.lol = new_lol_extend
        return self.object

    def form_valid(self, form):
        code = Invite.objects.filter(code=form.cleaned_data.get('code'))
        if code.exists():
            code = code[0]
            if not code.use:
                # code.use = True
                code.belong = self.object
                code.save()
                super(UserRegisterView, self).form_valid(form)
                self.create_extend()
                self.token = self.create_token()
                self.object.token = self.token
                self.object.set_password(form.cleaned_data.get('password'))
                self.object.save()
                return self.render_to_response(self.object)
            else:
                self.message = '邀请码已使用'
                self.status_code = ERROR_DATA
            return self.render_to_response(dict())
        else:
            self.message = '邀请码不存在'
            self.status_code = ERROR_DATA
            return self.render_to_response(dict())

    def form_invalid(self, form):
        super(UserRegisterView, self).form_invalid(form)
        self.status_code = ERROR_DATA
        self.message = json.loads(form.errors.as_json()).values()[0][0].get('message')
        return self.render_to_response(dict())

    def create_token(self):
        return string.join(
            random.sample('ZYXWVUTSRQPONMLKJIHGFEDCBA1234567890zyxwvutsrqponmlkjihgfedcbazyxwvutsrqponmlkjihgfedcba',
                          self.count)).replace(" ", "")


class UserThirdRegisterView(CheckSecurityMixin, StatusWrapMixin, JsonResponseMixin, CreateView):
    model = EUser
    form_class = UserThirdRegisterForm
    http_method_names = ['post']
    success_url = 'localhost'
    datetime_type = 'timestamp'
    include_attr = ['token', 'id', 'create_time', 'nick', 'phone', 'avatar']
    count = 64

    def create_extend(self):
        new_lol_extend = LOLInfoExtend()
        new_lol_extend.save()
        self.object.lol = new_lol_extend
        return self.object

    def form_valid(self, form):
        code = Invite.objects.filter(code=form.cleaned_data.get('code'))
        if code.exists():
            code = code[0]
            if not code.use:
                # code.use = True
                code.belong = self.object
                code.save()
                super(UserThirdRegisterView, self).form_valid(form)
                t_type = form.cleaned_data.get('type')
                if t_type == 1:
                    self.object.wechat_openid = form.cleaned_data.get('openid')
                    self.object.wechat_bind = True
                elif t_type == 2:
                    self.object.weibo_openid = form.cleaned_data.get('openid')
                    self.object.weibo_bind = True
                elif t_type == 3:
                    self.object.qq_openid = form.cleaned_data.get('openid')
                    self.object.qq_bind = True
                status, path = save_image(form.cleaned_data.get('avatar'), type='upload/lol',
                                          name='avatar{0}.{1}'.format(unicode(time.time()).replace('.', ''),
                                                                      form.cleaned_data.get('avatar').split('.')[-1]))
                if status:
                    self.object.avatar = path
                self.create_extend()
                self.token = self.create_token()
                self.object.token = self.token
                self.object.set_password(form.cleaned_data.get('password'))
                self.object.save()
                return self.render_to_response(self.object)
            else:
                self.message = '邀请码已使用'
                self.status_code = ERROR_DATA
            return self.render_to_response(dict())
        else:
            self.message = '邀请码不存在'
            self.status_code = ERROR_DATA
            return self.render_to_response(dict())

    def form_invalid(self, form):
        super(UserThirdRegisterView, self).form_invalid(form)
        self.status_code = ERROR_DATA
        self.message = json.loads(form.errors.as_json()).values()[0][0].get('message')
        return self.render_to_response(dict())

    def create_token(self):
        return string.join(
            random.sample('ZYXWVUTSRQPONMLKJIHGFEDCBA1234567890zyxwvutsrqponmlkjihgfedcbazyxwvutsrqponmlkjihgfedcba',
                          self.count)).replace(" ", "")


class UserResetView(CheckSecurityMixin, StatusWrapMixin, JsonResponseMixin, UpdateView):
    form_class = UserResetForm
    model = EUser
    http_method_names = ['post']
    success_url = 'localhost'
    datetime_type = 'timestamp'
    include_attr = ['token', 'id', 'create_time', 'nick', 'phone', 'avatar']
    pk_url_kwarg = 'phone'
    count = 64
    token = ''

    def create_token(self):
        return string.join(
            random.sample('ZYXWVUTSRQPONMLKJIHGFEDCBA1234567890zyxwvutsrqponmlkjihgfedcbazyxwvutsrqponmlkjihgfedcba',
                          self.count)).replace(" ", "")

    def form_invalid(self, form):
        super(UserResetView, self).form_invalid(form)
        self.status_code = ERROR_DATA
        self.message = json.loads(form.errors.as_json()).values()[0][0].get('message')
        return self.render_to_response(dict())

    def form_valid(self, form):
        if not self.object:
            return self.render_to_response(dict())
        super(UserResetView, self).form_valid(form)
        self.token = self.create_token()
        self.object.token = self.token
        self.object.set_password(form.cleaned_data.get('password'))
        self.object.save()
        return self.render_to_response(self.object)

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        pk = self.request.POST.get(self.pk_url_kwarg, None)
        queryset = queryset.filter(phone=pk)
        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            self.message = '帐号不存在'
            self.status_code = INFO_NO_EXIST
            return None
        return obj


class UserLoginView(CheckSecurityMixin, StatusWrapMixin, JsonResponseMixin, UpdateView):
    model = EUser
    form_class = UserLoginForm
    count = 64
    http_method_names = ['post']
    pk_url_kwarg = 'phone'
    datetime_type = 'timestamp'
    include_attr = ['token', 'id', 'create_time', 'nick', 'phone', 'avatar']
    success_url = 'localhost'
    token = ''

    def create_token(self):
        return string.join(
            random.sample('ZYXWVUTSRQPONMLKJIHGFEDCBA1234567890zyxwvutsrqponmlkjihgfedcbazyxwvutsrqponmlkjihgfedcba',
                          self.count)).replace(" ", "")

    def form_invalid(self, form):
        if not self.object:
            return self.render_to_response(dict())
        super(UserLoginView, self).form_invalid(form)
        self.status_code = ERROR_DATA
        self.message = json.loads(form.errors.as_json()).values()[0][0].get('message')
        return self.render_to_response(dict())

    def form_valid(self, form):
        if not self.object:
            return self.render_to_response(dict())
        super(UserLoginView, self).form_valid(form)
        if not self.object.check_password(form.cleaned_data.get('password')):
            self.message = '密码不正确'
            self.status_code = ERROR_PASSWORD
            return self.render_to_response(dict())
        self.token = self.create_token()
        # self.object.set_password(form.cleaned_data.get('password'))
        self.object.token = self.token
        self.object.save()
        return self.render_to_response(self.object)

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        pk = self.request.POST.get(self.pk_url_kwarg, None)
        queryset = queryset.filter(phone=pk)
        try:
            # Get the single item from the filtered queryset
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            self.message = '帐号不存在'
            self.status_code = INFO_NO_EXIST
            return None
        return obj


class UserLogoutView(CheckSecurityMixin, CheckTokenMixin, StatusWrapMixin, JsonResponseMixin, View):
    http_method_names = ['get']
    count = 64

    def create_token(self):
        return string.join(
            random.sample('ZYXWVUTSRQPONMLKJIHGFEDCBA1234567890zyxwvutsrqponmlkjihgfedcbazyxwvutsrqponmlkjihgfedcba',
                          self.count)).replace(" ", "")

    def get(self, request, *args, **kwargs):
        if not self.wrap_check_sign_result():
            return self.render_to_response(dict())
        if not self.wrap_check_token_result():
            return self.render_to_response(dict())
        self.user.token = self.create_token()
        self.user.save()
        return self.render_to_response(dict())


class UserChangePasswordView(CheckSecurityMixin, CheckTokenMixin, StatusWrapMixin, JsonResponseMixin, UpdateView):
    http_method_names = ['post']
    model = EUser
    success_url = 'localhost'
    form_class = UserChangePasswordForm

    def get_object(self, queryset=None):
        self.object = self.user
        return self.user

    def post(self, request, *args, **kwargs):
        if not self.wrap_check_sign_result():
            return self.render_to_response(dict())
        if not self.wrap_check_token_result():
            return self.render_to_response(dict())
        return super(UserChangePasswordView, self).post(request, *args, **kwargs)

    def form_invalid(self, form):
        super(UserChangePasswordView, self).form_invalid(form)
        self.status_code = ERROR_DATA
        self.message = json.loads(form.errors.as_json()).values()[0][0].get('message')
        return self.render_to_response(dict())

    def form_valid(self, form):
        super(UserChangePasswordView, self).form_valid(form)
        return self.render_to_response(dict())

    def get_form_kwargs(self):
        kwargs = super(UserChangePasswordView, self).get_form_kwargs()
        kwargs['user'] = self.user
        return kwargs


class UserThirdAccountBindView(CheckSecurityMixin, CheckTokenMixin, StatusWrapMixin, JsonResponseMixin, DetailView):
    http_method_names = ['post']
    model = EUser

    def post(self, request, *args, **kwargs):
        if not self.wrap_check_sign_result():
            return self.render_to_response(dict())
        if not self.wrap_check_token_result():
            return self.render_to_response(dict())
        t_type = request.POST.get('type')
        open_id = request.POST.get('openid')
        if t_type and open_id:
            if t_type == '1':
                self.user.wechat_openid = open_id
                self.user.wechat_bind = True
            elif t_type == '2':
                self.user.weibo_openid = open_id
                self.user.weibo_bind = True
            elif t_type == '3':
                self.user.qq_openid = open_id
                self.user.qq_bind = True
            self.user.save()
            return self.render_to_response(dict())
        self.message = '数据缺失'
        self.status_code = ERROR_DATA
        return self.render_to_response(dict())


class UserAvatarView(CheckSecurityMixin, CheckTokenMixin, StatusWrapMixin, JsonResponseMixin, DetailView):
    http_method_names = ['post']
    include_attr = ['id', 'create_time', 'nick', 'phone', 'avatar']
    datetime_type = 'timestamp'
    model = EUser

    def post(self, request, *args, **kwargs):
        if not self.wrap_check_sign_result():
            return self.render_to_response(dict())
        if not self.wrap_check_token_result():
            return self.render_to_response(dict())
        avatar = request.FILES.get('avatar')
        if avatar:
            s_path, full_path = upload_picture(avatar)
            self.user.avatar = s_path
            self.user.save()
            return self.render_to_response(self.user)
        self.message = '数据缺失'
        self.status_code = ERROR_DATA
        return self.render_to_response(dict())
