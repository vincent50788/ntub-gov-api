import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "topic_crawler.settings")

import django
django.setup()

import pytz
from apscheduler.schedulers.blocking import BlockingScheduler
from superCrawler import weatherCrawler
from superCrawler import oilCrawler

timez = pytz.timezone('Asia/Taipei')

scheduler = BlockingScheduler(timezone=timez)
scheduler.add_job(weatherCrawler, trigger='interval', minutes=20)
scheduler.add_job(oilCrawler, trigger='cron', hour='0-1', minute='0-59')
scheduler.start()


