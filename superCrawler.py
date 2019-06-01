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
from alerts.models import Alerts

dateTime_ = datetime.now() + timedelta(hours=8)
theTime = dateTime_.strftime('%H:%M')
theDate = dateTime_.strftime('%Y-%m-%d')


def weather_crawler():  # 環境Crawler
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
            Weathers.objects.filter(sitename=site_).update(county=county_, aqi=aqi_, status=status_, windspeed=windspeed_,
                                                            winddir=winddir_, date=date_, time=time_, longitude=longitude_, latitude=latitude_)
        else:
            Weathers.objects.create(sitename=site_, county=county_, aqi=aqi_, status=status_, windspeed=windspeed_,
                                    winddir=winddir_, date=date_, time=time_, longitude=longitude_, latitude=latitude_)
    print('weather_crawler')


def oil_crawler():  # oilCrawler
    url = "https://www.cpc.com.tw/Default.aspx"
    re = requests.get(url, verify=False)
    soup = BeautifulSoup(re.content)
    data = soup.find_all("div", class_="today_price_info")
    dic_ = {}
    for a in data:
        title = a.find("b", class_="name").text
        price = a.find("b", class_="price").text
        dic_[title] = float(price)

    if Oils.objects.all().exists():
        Oils.objects.all().update(unleaded=dic_['92無鉛'], super=dic_['95無鉛'], supreme=dic_['98無鉛'], alcohol_gas=dic_['酒精汽油'],
                                diesel=dic_['超級柴油'], liquefied_gas=dic_['液化石油氣'], date=theDate, time=theTime)
    else:
        Oils.objects.create(unleaded=dic_['92無鉛'], super=dic_['95無鉛'], supreme=dic_['98無鉛'], alcohol_gas=dic_['酒精汽油'],
                            diesel=dic_['超級柴油'], liquefied_gas=dic_['液化石油氣'], date=theDate, time=theTime)
    print('oil_crawler')


def alert_crawler():  # oilCrawler
    url = "https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/W-C0033-001?Authorization=CWB-242E2AA6-F542-43E1-973D-9A0A4DBB7E5E&downloadType=WEB&format=JSON"
    re = requests.get(url, verify=False)
    js = json.loads(re.content)
    data = js["cwbopendata"]["dataset"]["location"]
    for a in data:
        locationName = a['locationName']
        hazardConditions = a['hazardConditions']

        startTime, endTime, hazard, phenomena, affectedAreas = "", "", "", "", ""

        if type(hazardConditions) == dict:
            hazard = hazardConditions['hazards']['info']['phenomena']
            affectedAreas = hazardConditions['hazards']['hazard']['info']['affectedAreas']['location']['locationName']
            phenomena = hazardConditions['hazards']['hazard']['info']['phenomena']
            # startTime = hazardConditions['hazards']['validTime']['startTime']
            # endTime = hazardConditions['hazards']['validTime']['endTime']

        Alerts.objects.create(city=locationName, hazard=hazard, affectedareas=affectedAreas, phenomena=phenomena,
                                  date=theDate, time=theTime)


alert_crawler()
