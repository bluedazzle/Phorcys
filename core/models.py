# coding: utf-8
from __future__ import unicode_literals

from django.db import models


# Create your models here.

class BaseModel(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    modify_time = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Country(BaseModel):
    name = models.CharField(max_length=30, unique=True)
    flag = models.CharField(max_length=100, default='')

    def __unicode__(self):
        return '{0}-{1}'.format(self.name, self.id)


class BaseNews(BaseModel):
    news_choice = [
        (1, '小图'),
        (2, '大图'),
        (3, '文字')
    ]

    title = models.CharField(max_length=100)
    picture1 = models.CharField(max_length=200, null=True, blank=True)
    picture2 = models.CharField(max_length=200, null=True, blank=True)
    picture3 = models.CharField(max_length=200, null=True, blank=True)
    content = models.TextField()
    views = models.IntegerField(default=0)
    publish = models.BooleanField(default=False)
    news_type = models.IntegerField(default=1, choices=news_choice)
    url = models.CharField(max_length=100, default='')

    class Meta:
        abstract = True


class BaseTournament(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    start_time = models.DateField()
    end_time = models.DateField()
    thumb = models.IntegerField(default=0)
    cover = models.CharField(default='', max_length=100)

    class Meta:
        abstract = True


class BaseComment(BaseModel):
    content = models.TextField()
    thumb = models.IntegerField(default=0)

    class Meta:
        abstract = True


class BasePlayer(BaseModel):
    name = models.CharField(max_length=50)
    nick = models.CharField(max_length=50)
    avatar = models.CharField(default='http://www.fibar.cn', max_length=100)
    nationality = models.ForeignKey(Country, related_name='country_players', on_delete=models.SET_NULL, null=True, blank=True)
    intro = models.TextField(default='')

    class Meta:
        abstract = True


class BaseTopic(BaseModel):
    title = models.CharField(max_length=100)
    content = models.TextField()
    thumb = models.IntegerField(default=0)

    class Meta:
        abstract = True


class BaseWeibo(BaseModel):
    title = models.CharField(max_length=100)
    content = models.TextField()
    thumb = models.IntegerField(default=0)

    class Meta:
        abstract = True


class BaseTeam(BaseModel):
    abbreviation = models.CharField(max_length=20)
    name = models.CharField(max_length=100)
    logo = models.CharField(default='http://www.fibar.cn', max_length=100)
    info = models.TextField()
    country = models.ForeignKey(Country, related_name='country_teams', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        abstract = True


class Secret(BaseModel):
    secret = models.CharField(max_length=64)
    info = models.CharField(max_length=20, default='system')

    def __unicode__(self):
        return self.info