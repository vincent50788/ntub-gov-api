import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "topic_crawler.settings")

import django
django.setup()

from apscheduler.schedulers.blocking import BlockingScheduler
from weathersCrawler import insert

scheduler = BlockingScheduler()  # 定時程序
scheduler.add_job(insert, trigger='interval', minutes=2)
scheduler.start()


