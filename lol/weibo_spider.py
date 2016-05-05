# coding: utf-8

from __future__ import unicode_literals

import json

from weibo import Client

from lol.models import SpiderConfig, Weibo, Player, Team

LAST_ID = '3971743075208972'


def get_data(since_id=None):
    c = Client('1640210542', '9f07ec94c83c1249adf7b37964a610da',
               'http://rapospectre.com',
               username='rapospectre@163.com',
               password='123456qq')
    if since_id and since_id != '':
        data = c.get('statuses/home_timeline', count=10, since_id=since_id)
    else:
        data = c.get('statuses/home_timeline', count=10)
    next_id = data.get('next_cursor')
    content = data.get('statuses')
    for itm in content:
        mid = unicode(itm.get('mid'))
        if Weibo.objects.filter(mid=mid).exists():
            continue
        uid = unicode(itm.get('user').get('id'))
        player = Player.objects.filter(wid=uid)
        if player.exists():
            player = player[0]
            Weibo(wid=mid,
                  content=json.dumps(itm),
                  player_author=player).save()
        else:
            team = Team.objects.filter(wid=uid)
            if team.exists():
                team = team[0]
                Weibo(wid=mid,
                      content=json.dumps(itm),
                      team_author=team,
                      type=2).save()
    if next_id == since_id:
        config = SpiderConfig.objects.all()[0]
        config.since_id = next_id
        config.save()
        return True
    get_data(next_id)


# get_data('')