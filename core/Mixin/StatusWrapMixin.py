# coding: utf-8
from __future__ import unicode_literals
from django.http import HttpResponse

# Info Code
ERROR_UNKNOWN = 0
INFO_SUCCESS = 1
ERROR_PERMISSION_DENIED = 2
ERROR_ACCOUNT_NO_EXIST = 3
ERROR_TOKEN = 3
ERROR_DATA = 4
ERROR_PASSWORD = 5
INFO_EXISTED = 6
INFO_NO_EXIST = 7
INFO_EXPIRE = 8
INFO_NO_VERIFY = 10
ERROR_VERIFY = 11


class StatusWrapMixin(object):
    status_code = INFO_SUCCESS
    message = 'success'

    def render_to_response(self, context, **response_kwargs):
        context_dict = self.context_serialize(context)
        json_context = self.json_serializer(self.wrapper(context_dict))
        return HttpResponse(json_context, content_type='application/json', **response_kwargs)

    def wrapper(self, context):
        return_data = dict()
        return_data['body'] = context
        return_data['status'] = self.status_code
        return_data['msg'] = self.message
        if self.status_code != INFO_SUCCESS:
            return_data['body'] = {}
        return return_data
