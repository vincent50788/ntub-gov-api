import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "topic_crawler.settings")

import django
django.setup()

import pytz
from apscheduler.schedulers.blocking import BlockingScheduler
from superCrawler import *


timez = pytz.timezone('Asia/Taipei')

scheduler = BlockingScheduler(timezone=timez)
scheduler.add_job(weather_crawler, trigger='interval', minutes=20)
scheduler.add_job(oil_crawler, trigger='cron', hour='0-1', minute='0-59')
scheduler.add_job(alert_crawler, trigger='interval', minute=5)
scheduler.start()


