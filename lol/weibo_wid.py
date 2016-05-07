# coding: utf-8

from __future__ import unicode_literals

from lol.models import Team, Player


def get_team_wid():
    with open('lol/team.txt', 'r') as f1:
        for line in f1.readlines():
            abbreviation, wid = unicode(line).split(',')
            team = Team.objects.filter(abbreviation__iexact=abbreviation)
            if team.exists():
                team = team[0]
                team.wid = wid
                team.save()
            else:
                print '{0}未找到'.format(abbreviation).encode('utf-8')
    print '队伍id匹配完毕'.encode('utf-8')


def get_player_wid():
    with open('lol/player.txt', 'r') as f1:
        for line in f1.readlines():
            nick, wid = unicode(line).split(',')
            team = Player.objects.filter(nick__iexact=nick)
            if team.exists():
                team = team[0]
                team.wid = wid
                team.save()
            else:
                print '{0}未找到'.format(nick).encode('utf-8')
    print '选手id匹配完毕'.encode('utf-8')
