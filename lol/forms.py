# coding: utf-8
from __future__ import unicode_literals
import datetime

from django.core.validators import EmailValidator
from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm
from django import forms
from django.utils.timezone import get_current_timezone

from lol.models import News, NewsComment, TopicComment, WeiboComment, TournamentComment


class NewsCommentForm(forms.ModelForm):
    """
    新闻评论Form
    """

    def save(self, commit=False):
        return super(NewsCommentForm, self).save(commit=commit)

    class Meta:
        model = NewsComment
        fields = ['content']


class TopicCommentForm(forms.ModelForm):
    """
    社区评论Form
    """

    def save(self, commit=False):
        return super(TopicCommentForm, self).save(commit=commit)

    class Meta:
        model = TopicComment
        fields = ['content']


class WeiboCommentForm(forms.ModelForm):
    """
    微博评论Form
    """

    def save(self, commit=False):
        return super(WeiboCommentForm, self).save(commit=commit)

    class Meta:
        model = WeiboComment
        fields = ['content']


class TournamentCommentForm(forms.ModelForm):
    """
    联赛评论Form
    """

    def save(self, commit=False):
        return super(TournamentCommentForm, self).save(commit=commit)

    class Meta:
        model = TournamentComment
        fields = ['content']
