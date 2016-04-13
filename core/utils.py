# coding: utf-8
from __future__ import unicode_literals

import hashlib

import requests

from Phorcys.settings import BASE_DIR
from core.models import Secret

import random
import string


def create_secret(count=64):
    return string.join(
        random.sample('''ZYXWVUTSRQPONMLKJIHGFEDCBA1234567890zyxwvutsrqponmlkjihgfedcbazyxwvutsrqponmlkjihgfedcba''',
                      count)).replace(" ", "")


def create_token(count=32):
    return string.join(
        random.sample('''ZYXWVUTSRQPONMLKJIHGFEDCBA1234567890zyxwvutsrqponmlkjihgfedcba''',
                      count)).replace(" ", "")


def check_sign(timestamp, sign):
    secret = Secret.objects.all()[0].secret
    check = unicode(hashlib.md5('{0}{1}'.format(timestamp, secret)).hexdigest()).upper()
    if check == unicode(sign).upper():
        return True
    return False


def save_image(url, type='lol/hero', name="default.jpg"):
    dir_path = '/static/image/{0}/{1}'.format(type, name)
    save_path = '{0}{1}'.format(BASE_DIR, dir_path)
    response = requests.get(url, stream=True)
    image = response.content
    try:
        with open(save_path, "wb") as jpg:
            jpg.write(image)
            return True, dir_path
    except IOError:
        print("IO Error\n")
        return False, None
    finally:
        jpg.close
