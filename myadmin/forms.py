# coding: utf-8

from __future__ import unicode_literals
from django import forms


class AdminLoginForm(forms.Form):
    username_error_messages = {
        'required': '请输入帐号',
        'max_length': '请输入11位手机号',
        'min_length': '请输入11位手机号',
    }
    username = forms.CharField(max_length=11, min_length=11, error_messages=username_error_messages)
    password = forms.CharField(max_length=50)

