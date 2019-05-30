from apscheduler.schedulers.blocking import BlockingScheduler
from weathersCrawler import insert

scheduler = BlockingScheduler()  # 定時程序
scheduler.add_job(insert, trigger='interval', minutes=2)
scheduler.start()
