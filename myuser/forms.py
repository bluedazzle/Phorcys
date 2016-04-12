# coding: utf-8
from __future__ import unicode_literals

from django import forms
from django.contrib.auth.hashers import make_password

from myuser.models import Verify, EUser

import datetime
from django.utils.timezone import get_current_timezone


class VerifyCodeForm(forms.ModelForm):
    error_messages = {
        'min_time': '请求短信时间间隔过短',
        'required': '请输入手机号',
        'phone_format': '请输入11位手机号',
    }

    phone = forms.CharField(max_length=11, error_messages=error_messages)

    def clean_phone(self):
        phone = unicode(self.cleaned_data.get('phone', None))
        if phone:
            if len(phone) != 11:
                raise forms.ValidationError(message=self.error_messages['phone_format'], code='phone_format')
            phone_list = Verify.objects.filter(phone=phone).order_by('-create_time')
            if phone_list.exists():
                phone_obj = phone_list[0]
                now_time = datetime.datetime.now(tz=get_current_timezone())
                if now_time - phone_obj.create_time < datetime.timedelta(seconds=30):
                    raise forms.ValidationError(message=self.error_messages['min_time'], code='min_time')
                else:
                    return phone
            else:
                return phone
        else:
            raise forms.ValidationError(message=self.error_messages['required'], code='required')

    def save(self, commit=False):
        return super(VerifyCodeForm, self).save(commit)

    class Meta:
        model = Verify
        fields = ['phone']


class UserRegisterForm(forms.ModelForm):
    phone_error_messages = {
        'required': '请输入手机号',
        'unique': '帐号已存在',
        'phone_format': '请输入11位手机号',
    }

    nick_error_messages = {
        'required': '请输入昵称',
        'unique': '昵称已存在',
    }

    password_error_messages = {
        'required': '请输入密码',
        'min_length': '请至少输入6位以上密码',
    }

    phone = forms.CharField(max_length=11, error_messages=phone_error_messages)
    nick = forms.CharField(max_length=20, error_messages=nick_error_messages)
    password = forms.CharField(max_length=100, error_messages=password_error_messages)

    def clean_password(self):
        password = unicode(self.cleaned_data.get('password'))
        if len(password) < 6:
            raise forms.ValidationError(message=self.password_error_messages['min_length'], code='min_length')
        return password

    def clean_phone(self):
        phone = unicode(self.cleaned_data.get('phone', None))
        if len(phone) != 11:
            raise forms.ValidationError(message=self.phone_error_messages['phone_format'], code='phone_format')
        return phone

    def save(self, commit=False):
        return super(UserRegisterForm, self).save(commit)

    class Meta:
        model = EUser
        fields = ['phone', 'nick']


class UserResetForm(forms.ModelForm):
    password_error_messages = {
        'required': '请输入密码',
        'min_length': '请至少输入6位以上密码',
    }
    password = forms.CharField(max_length=100, error_messages=password_error_messages)

    def clean_password(self):
        password = unicode(self.cleaned_data.get('password'))
        if len(password) < 6:
            raise forms.ValidationError(message=self.password_error_messages['min_length'], code='min_length')
        return password

    def save(self, commit=False):
        return super(UserResetForm, self).save(commit)

    class Meta:
        model = EUser
        fields = ['password']


class UserLoginForm(forms.ModelForm):
    password_error_messages = {
        'required': '请输入密码',
        'min_length': '请至少输入6位以上密码',
    }
    password = forms.CharField(max_length=100, error_messages=password_error_messages)

    def save(self, commit=False):
        return super(UserLoginForm, self).save(commit)

    class Meta:
        model = EUser
        fields = []
