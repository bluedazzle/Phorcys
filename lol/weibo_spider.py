# coding: utf-8

from __future__ import unicode_literals
from weibo import Client

LAST_ID = '3971743075208972'


def get_data(since_id=None):
    c = Client('1640210542', '9f07ec94c83c1249adf7b37964a610da',
               'http://rapospectre.com',
               username='rapospectre@163.com',
               password='123456qq')
    if since_id:
        data = c.get('statuses/home_timeline', count=10, since_id=since_id)
    else:
        data = c.get('statuses/home_timeline', count=10)
    next_id = data.get('next_cursor')
    if next_id == since_id:
        # 存入 since_id
        LAST_ID = next_id
        print LAST_ID
        return True
    content = data.get('statuses')
    for itm in content:
        print itm.get('text')

    get_data(next_id)


# get_data(3971746875249353)

import datetime

print datetime.date.today()