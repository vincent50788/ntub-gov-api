# 單獨執行.pyError
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "topic_crawler.settings")

import django
django.setup()
# package
import json
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
# DB
from weathers.models import Weathers
from oils.models import Oils
from alerts.models import Alerts

dateTime_ = datetime.now() + timedelta(hours=8)
theTime = dateTime_.strftime('%H:%M')
theDate = dateTime_.strftime('%Y-%m-%d')


def weather_crawler():
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

        Weathers.objects.filter(sitename=site_).update(county=county_, aqi=aqi_, status=status_, windspeed=windspeed_,
                                                       winddir=winddir_, date=date_, time=time_, longitude=longitude_,
                                                       latitude=latitude_)
'''
        Weathers.objects.create(sitename=site_, county=county_, aqi=aqi_, status=status_, windspeed=windspeed_, 
                                winddir=winddir_, date=date_, time=time_, longitude=longitude_, latitude=latitude_)
'''


def oil_crawler():
    url = "https://www.cpc.com.tw/GetOilPriceJson.aspx?type=TodayOilPriceString"
    # url = "https://www2.moeaboe.gov.tw/oil102/oil2017/newmain.asp"
    re = requests.get(url, verify=False)
    js = json.loads(re.content)
    unleaded = js['sPrice1']
    super_ = js['sPrice2']
    supreme = js['sPrice3']
    alcohol_gas = js['sPrice4']
    diesel = js['sPrice5']
    liquefied_gas = js['sPrice6']

    print(unleaded, super_, supreme, alcohol_gas, diesel, liquefied_gas)

    Oils.objects.all().update(unleaded= unleaded, super=super_, supreme=supreme, alcohol_gas=alcohol_gas,
                              diesel=diesel, liquefied_gas=liquefied_gas, date=theDate, time=theTime)


def alert_crawler():
    url = "https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/W-C0033-001?Authorization=CWB-242E2AA6-F542-43E1-973D-9A0A4DBB7E5E&downloadType=WEB&format=JSON"
    re = requests.get(url, verify=False)
    js = json.loads(re.content)
    data = js["cwbopendata"]["dataset"]["location"]
    for a in data:
        locationName = a['locationName']  # 地點
        hazardConditions = a['hazardConditions']  # 警報情形dic

        startTime, endTime, hazard, phenomena, affectedAreas = "", "", "", "", ""

        if type(hazardConditions) == dict:  # 如果有警報
            hazard = hazardConditions['hazards']['info']['phenomena']  # 警報情況 大雨

            # startTime = hazardConditions['hazards']['validTime']['startTime']  # 警報有效時間
            # endTime = hazardConditions['hazards']['validTime']['endTime']

        # Alerts.objects.create(city=locationName, hazard=hazard, affectedareas=affectedAreas, phenomena=phenomena,
                                    # date=theDate, time=theTime)

        Alerts.objects.filter(city=locationName).update(hazard=hazard, date=theDate, time=theTime)


