from django.contrib import admin
from myuser.models import EUser, Verify, Invite, FeedBack
from lol.models import LOLInfoExtend

# Register your models here.

admin.site.register(EUser)
admin.site.register(LOLInfoExtend)
admin.site.register(Verify)
admin.site.register(Invite)
admin.site.register(FeedBack)
