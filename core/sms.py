# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import requests

SMS_ACCOUNT = 'jiang-01'
SMS_PASSWD = 'Txb123456'


def send_msg(phone, verify):
    req_url = 'http://222.73.117.156:80/msg/HttpBatchSendSM?' \
              'account=%(account)s&pswd=%(password)s&mobile=%(phone)s&msg' \
              '=您的验证码是：%(verify)s&needstatus=true' % {'account': SMS_ACCOUNT, 'password': SMS_PASSWD, 'phone': phone,
                                                      'verify': verify}
    result = requests.get(req_url)
    rescode = str(result.content)[0:16].split(',')[1]
    print result.content
    if str(rescode) == '0':
        return True
    else:
        return False
