# coding: utf-8

from __future__ import unicode_literals

import hashlib

from core.Mixin.StatusWrapMixin import ERROR_PERMISSION_DENIED, ERROR_TOKEN
from core.models import Secret
from myuser.models import EUser


class CheckSecurityMixin(object):
    secret = None

    def get_current_secret(self):
        self.secret = Secret.objects.all()[0].secret
        return self.secret

    def check_sign(self):
        timestamp = self.request.GET.get('timestamp', '')
        sign = unicode(self.request.GET.get('sign', '')).upper()
        check = unicode(hashlib.md5('{0}{1}'.format(timestamp, self.secret)).hexdigest()).upper()
        if check == sign:
            return True
        return False

    def wrap_check_sign_result(self):
        self.get_current_secret()
        result = self.check_sign()
        if not result:
            self.message = 'sign 验证失败'
            self.status_code = ERROR_PERMISSION_DENIED
            return False
        return True

    def get(self, request, *args, **kwargs):
        if not self.wrap_check_sign_result():
            return self.render_to_response(dict())
        return super(CheckSecurityMixin, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if not self.wrap_check_sign_result():
            return self.render_to_response(dict())
        return super(CheckSecurityMixin, self).post(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        if not self.wrap_check_sign_result():
            return self.render_to_response(dict())
        return super(CheckSecurityMixin, self).put(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        if not self.wrap_check_sign_result():
            return self.render_to_response(dict())
        return super(CheckSecurityMixin, self).patch(request, *args, **kwargs)


class CheckTokenMixin(object):
    token = None
    user = None

    def get_current_token(self):
        self.token = self.request.GET.get('token', '')
        return self.token

    def check_token(self):
        self.get_current_token()
        user_list = EUser.objects.filter(token=self.token)
        if user_list.exists():
            self.user = user_list[0]
            return True
        return False

    def wrap_check_token_result(self):
        result = self.check_token()
        if not result:
            self.message = 'token 错误, 请重新登陆'
            self.status_code = ERROR_TOKEN
            return False
        return True