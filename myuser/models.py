# coding: utf-8

from __future__ import unicode_literals

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser
from django.db import models

from core.models import BaseModel


# Create your models here.

class EUser(BaseModel, AbstractBaseUser):
    from lol.models import LOLInfoExtend

    phone = models.CharField(max_length=13, unique=True)
    nick = models.CharField(max_length=200, unique=True)
    avatar = models.CharField(max_length=200, null=True, blank=True)
    token = models.CharField(max_length=64)
    forbid = models.BooleanField(default=False)
    wechat_openid = models.CharField(max_length=64, null=True, blank=True)
    wechat_bind = models.BooleanField(default=False)
    weibo_openid = models.CharField(max_length=64, null=True, blank=True)
    weibo_bind = models.BooleanField(default=False)
    qq_openid = models.CharField(max_length=64, null=True, blank=True)
    qq_bind = models.BooleanField(default=False)

    lol = models.OneToOneField('lol.LOLInfoExtend', related_name='lol_info_user', null=True, blank=True)

    USERNAME_FIELD = 'phone'

    # def check_password(self, raw_password):
    #     if self.password == raw_password:
    #         return True
    #     return False

    def __unicode__(self):
        return '{0}-{1}'.format(self.phone, self.nick)


class Verify(BaseModel):
    code = models.CharField(max_length=10)
    phone = models.CharField(max_length=13)

    def __unicode__(self):
        return self.phone


class Invite(BaseModel):
    code = models.CharField(max_length=6)
    use = models.BooleanField(default=False)
    belong = models.ForeignKey(EUser, related_name='user_invite', null=True, blank=True)

    def __unicode__(self):
        return self.code


class FeedBack(BaseModel):
    content = models.TextField()
    author = models.ForeignKey(EUser, related_name='user_feedbacks', null=True, blank=True, on_delete=models.SET_NULL)
    read = models.BooleanField(default=False)

    def __unicode__(self):
        return self.author.phone
