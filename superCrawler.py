# 單獨執行.pyError
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "topic_crawler.settings")

import django
django.setup()

import json
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from weathers.models import Weathers  # weathersDB
from oils.models import Oils  # oilsDB


def weatherCrawler():  # 環境Crawler
    url = "https://opendata.epa.gov.tw/webapi/Data/REWIQA/?$orderby=SiteName&$skip=0&$top=1000&format=json"
    re = requests.get(url, verify=False)
    js = json.loads(re.content)
    for a in js:
        site_ = a['SiteName']  # 測站名稱
        county_ = a['County']  # 地區
        aqi_ = (a['AQI'])
        status_ = a['Status']  # 品質狀態
        windspeed_ = a['WindSpeed']  # 風速
        winddir_ = a['WindDirec']  # 風向
        date_ = a['PublishTime'].split(' ')[0]
        time_ = a['PublishTime'].split(' ')[1]
        longitude_ = a['Longitude']
        latitude_ = a['Latitude']

        if aqi_ == "":
            aqi_ = 0

        if winddir_ == "":
            winddir_ = 0

        if windspeed_ == "":
           windspeed_ = 0

        if Weathers.objects.all().exists():
            Weathers.objects.all().update(sitename=site_, county=county_, aqi=aqi_, status=status_, windspeed=windspeed_
                                          , winddir=winddir_, date=date_, time=time_, longitude=longitude_, latitude=latitude_)
        else:
            Weathers.objects.create(sitename=site_, county=county_, aqi=aqi_, status=status_, windspeed=windspeed_,
                                    winddir=winddir_, date=date_, time=time_, longitude=longitude_, latitude=latitude_)

    print('the end')


def oilCrawler():  # oilCrawler
    url = "https://www.cpc.com.tw/Default.aspx"
    re = requests.get(url, verify=False)
    soup = BeautifulSoup(re.content)
    data = soup.find_all("div", class_="today_price_info")
    dic_ = {}
    for a in data:
        title = a.find("b", class_="name").text
        price = a.find("b", class_="price").text
        dic_[title] = float(price)

    dateTime_ = datetime.now() + timedelta(hours=8)
    theTime = dateTime_.strftime('%H:%M')
    theDate = dateTime_.strftime('%Y-%m-%d')

    if Oils.objects.all().exists():
        Oils.objects.all().update(unleaded=dic_['92無鉛'], super=dic_['95無鉛'], supreme=dic_['98無鉛'], alcohol_gas=dic_['酒精汽油'],
                            diesel=dic_['超級柴油'], liquefied_gas=dic_['液化石油氣'], date=theDate, time=theTime)
    else:
        Oils.objects.create(unleaded=dic_['92無鉛'], super=dic_['95無鉛'], supreme=dic_['98無鉛'], alcohol_gas=dic_['酒精汽油'],
                            diesel=dic_['超級柴油'], liquefied_gas=dic_['液化石油氣'], date=theDate, time=theTime)
    print('uuuu')


