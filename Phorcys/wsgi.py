"""
WSGI config for Phorcys project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os
# import uwsgi

from lol.weibo_spider import get_data

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Phorcys.settings")

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

# uwsgi.register_signal(80, "weibo worker", get_data)
# uwsgi.add_cron(80, 30, -1, -1, -1, -1)
