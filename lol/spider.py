# coding: utf-8
from  __future__ import unicode_literals

import json

import requests
from bs4 import BeautifulSoup
from core.utils import save_image
from lol.models import Equipment, Hero, SummonerSpells, Position, Team, Player
from core.models import Country


def get_equipment():
    url = 'http://cha.17173.com/lol/items.html'
    res = requests.get(url)
    res = res.text.encode('ISO-8859-1').decode('utf-8')
    soup = BeautifulSoup(res)
    ul = soup.findAll('ul', attrs={'class': 'games_list games_item_list'})
    li_list = ul[0].findAll('li')
    print 'total {0} equipments'.format(len(li_list))
    for li in li_list:
        name = unicode(li.find('a').attrs.get('title'))
        if Equipment.objects.filter(name=name).exists():
            continue
        new_equip = Equipment()
        new_equip.name = name
        url = unicode(li.find('a').find('img').attrs.get('src'))
        name = url.split('/')[-1]
        status, path = save_image(url, type='lol/equipment', name=name)
        if status:
            new_equip.picture = path
        new_equip.save()


def get_hero():
    url = 'http://cha.17173.com/lol/'
    res = requests.get(url)
    res = res.text.encode('ISO-8859-1').decode('utf-8')
    soup = BeautifulSoup(res)
    ul = soup.findAll('ul', attrs={'class': 'games_list'})
    li_list = ul[0].findAll('li')
    print 'total {0} heros'.format(len(li_list))
    for li in li_list:
        hid = unicode(li.find('a').attrs.get('tipurl')).split('/')[-1]
        detail_url = 'http://cha.17173.com/lol/tips.html?c=UTF-8&t=details&l=zhCN&id={0}'.format(hid)
        res = requests.get(detail_url)
        res = res.text.encode('ISO-8859-1').decode('utf-8')
        soup = BeautifulSoup(res)
        content = soup.find('div', attrs={'class': 'tips_1'})
        hero = content.find('h6').find('span').text
        name = content.find('h6').text.replace(hero, '')
        if Hero.objects.filter(hero=hero).exists():
            continue
        pic = unicode(content.find('img').attrs.get('src'))
        new_hero = Hero()
        new_hero.hero = hero
        new_hero.name = name
        img_name = pic.split('/')[-1]
        status, path = save_image(pic, type='lol/hero', name=img_name)
        if status:
            new_hero.picture = path
        new_hero.save()


def get_summoner():
    url = 'http://cha.17173.com/lol/summoners.html'
    res = requests.get(url)
    res = res.text.encode('ISO-8859-1').decode('utf-8')
    soup = BeautifulSoup(res)
    ul = soup.findAll('ul', attrs={'class': 'skills line_class'})
    li_list = ul[0].findAll('li')
    print 'total {0} summoners'.format(len(li_list))
    for li in li_list:
        pic = unicode(li.find('div', attrs={'class': 'skills_info'}).find('img').attrs.get('src'))
        name = unicode(li.find('div', attrs={'class': 'skills_info'}).find('div').find('h6').text)
        if SummonerSpells.objects.filter(name=name).exists():
            continue
        img_name = pic.split('/')[-1]
        new_summoner = SummonerSpells()
        new_summoner.name = name
        status, path = save_image(pic, type='lol/summoner', name=img_name)
        if status:
            new_summoner.picture = path
        new_summoner.save()


def get_area():
    areas = [
        {'name': '港澳台', 'flag': '/s/image/area/1.png'},
        {'name': '中国', 'flag': '/s/image/area/1.png'},
        {'name': '韩国', 'flag': '/s/image/area/2.png'},
        {'name': '欧洲', 'flag': '/s/image/area/3.png'},
        {'name': '北美', 'flag': '/s/image/area/4.png'},
        {'name': '其他', 'flag': '/s/image/area/6.png'},
        {'name': '未知', 'flag': '/s/image/area/7.png'},
    ]
    for itm in areas:
        try:
            new_area = Country(name=itm['name'], flag=itm['flag'])
            new_area.save()
        except Exception, e:
            continue


def get_position():
    titles = ['中单', 'ADC', '上单', '辅助', '打野']
    for itm in titles:
        try:
            new_position = Position(title=itm)
            new_position.save()
        except Exception, e:
            continue


def get_teams():
    total = 0
    area_list = ['未知', '中国', '韩国', '欧洲', '北美', '港澳台', '其他']
    for i in range(1, 7):
        url = 'http://lol.766.com/db/lol/team/list?areaId={0}'.format(i)
        res = json.loads(requests.get(url).text)
        total += len(res)
        for item in res:
            name = item.get('name', '')
            if Team.objects.filter(name=name).exists():
                continue
            new_team = Team()
            new_team.name = name
            new_team.abbreviation = item.get('abbreviation', '')
            new_team.info = item.get('description', '')
            new_team.country = Country.objects.get(name=area_list[i])
            logo = unicode(item.get('team_icon'))
            if logo:
                img_name = logo.split('/')[-1]
                status, path = save_image(logo, type='lol/team', name=img_name)
                new_team.logo = path
            new_team.save()
    print 'total {0} teams'.format(total)


def get_players():
    total = 0
    area_id = {'81': '中国', '49': '韩国'}
    postition_id = ['未知', '上单', '打野', '中单', 'ADC', '辅助']
    offset = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
              'v', 'w', 'x', 'y', 'z']
    for i in offset:
        url = 'http://lol.766.com/db/lol/player/list?areaId=0&prefix={0}'.format(i)
        res = json.loads(requests.get(url).text)
        total += len(res)
        for item in res:
            nick = item.get('gameName')
            if Player.objects.filter(nick=nick).exists():
                continue
            new_player = Player(nick=nick)
            ptype = int(item.get('gamePositionId', '1'))
            if ptype not in range(1, 6):
                ptype = 1
            new_player.position = Position.objects.get(title=postition_id[ptype])
            team_name = item.get('teamName')
            if team_name:
                team = Team.objects.filter(abbreviation=team_name)
                if team.exists():
                    new_player.belong = team[0]
            icon = unicode(item.get('icon'))
            if icon:
                img_name = icon.split('/')[-1]
                status, path = save_image(icon, type='lol/player', name=img_name)
                if status:
                    new_player.avatar = path
            new_player.save()
    print 'total {0} players'.format(total)
