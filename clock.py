import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "topic_crawler.settings")

import django
django.setup()

import pytz
from apscheduler.schedulers.blocking import BlockingScheduler
from superCrawler import *
import requests

timez = pytz.timezone('Asia/Taipei')  # 台北時區


def time_to_getup():
    print("wakeup 10 minutes")
    url = 'https://topic-ntub.herokuapp.com/'
    re = requests.get(url)
    print(re)


scheduler = BlockingScheduler(timezone=timez)

scheduler.add_job(time_to_getup, 'interval', minutes=10)
scheduler.add_job(weather_crawler, trigger='interval', minutes=20)
scheduler.add_job(aqi_crawler, trigger='interval', minutes=20)
scheduler.add_job(oil_crawler, trigger='cron', hour='0-1', minute='0-59')
scheduler.add_job(alert_crawler, 'interval', minutes=5)

scheduler.start()



