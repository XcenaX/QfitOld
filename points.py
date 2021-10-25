import os, sys, time
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE','qfit.settings')
django.setup()

from api.models import *
from datetime import datetime
import json
import time
from django.utils import timezone

from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

@sched.scheduled_job('cron', month='1-12', day='1', hour='0')
def scheduled_job():
    for user in User.objects.all():
        user.give_bonuses()
        print(user.name)
    

sched.start()


