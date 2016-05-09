# coding: utf-8

from __future__ import unicode_literals

import json

from weibo import Client

from lol.models import SpiderConfig, Weibo, Player, Team


def get_data(since_id=None):
    if since_id is None:
        since_id = SpiderConfig.objects.all()[0].since_id
    c = Client('335303971', 'd6423ea88ea9dd9121eadf8e791f8cb2',
               'http://rapospectre.com',
               username='1806962021@qq.com',
               password='forever-_419')
    if since_id and since_id != '':
        data = c.get('statuses/home_timeline', count=150, since_id=since_id)
    else:
        data = c.get('statuses/home_timeline', count=150)
    next_id = data.get('next_cursor')
    content = data.get('statuses')
    for itm in content:
        mid = unicode(itm.get('mid'))
        if Weibo.objects.filter(wid=mid).exists():
            break
        uid = unicode(itm.get('user').get('id')).strip()
        # print itm.get('user').get('screen_name')
        player = Player.objects.filter(wid=uid)
        if player.exists():
            player = player[0]
            Weibo(wid=mid,
                  content=itm,
                  player_author=player).save()
        else:
            team = Team.objects.filter(wid=uid)
            if team.exists():
                team = team[0]
                Weibo(wid=mid,
                      content=itm,
                      team_author=team,
                      type=2).save()
    if next_id == since_id:
        config = SpiderConfig.objects.all()[0]
        config.since_id = next_id
        config.save()
        return True
    get_data(next_id)
