# 單獨執行.pyError
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "topic_crawler.settings")

import django
django.setup()
# package
import json
import requests
from datetime import datetime, timedelta

# DB
from aqi_quality.models import AqiQuality
from oils.models import Oils
from alerts.models import Alerts

dateTime_ = datetime.now() + timedelta(hours=8)
theTime = dateTime_.strftime('%H:%M')
theDate = dateTime_.strftime('%Y-%m-%d')


def aqi_crawler():
    url = "https://opendata.epa.gov.tw/webapi/Data/REWIQA/?$orderby=SiteName&$skip=0&$top=1000&format=json"
    re = requests.get(url, verify=False)
    js = json.loads(re.content)

    for a in js:
        site = a['SiteName']  # 測站名稱
        county = a['County']  # 地區
        aqi = a['AQI']
        pollutant = a['Pollutant']
        status = a['Status']  # 品質狀態
        pmten = a['PM10']
        pmtwo = a['PM2.5']
        wind_speed = a['WindSpeed']  # 風速
        wind_dic = a['WindDirec']  # 風向
        pmten_avg = a['PM10_AVG']
        pmtwo_avg = a['PM2.5_AVG']
        longitude = a['Longitude']
        latitude = a['Latitude']
        date = a['PublishTime'].split(' ')[0]
        time = a['PublishTime'].split(' ')[1]

        if aqi == "":
            aqi = "0"
        else:
            aqi = str(aqi)
        if pmten == "":
            pmten = "0"
        else:
            pmten = str(pmten)
        if pmtwo == "":
            pmtwo = "0"
        else:
            pmtwo = str(pmten)
        if pmten == "":
            pmten = "0"
        else:
            pmten = str(pmten)
        if wind_dic == "":
            wind_dic = "0"
        else:
            wind_dic = str(wind_dic)
        if wind_speed == "":
            wind_speed = "0"
        else:
            wind_speed = float(wind_speed)
        if pmtwo_avg == "":
            pmtwo_avg = "0"
        else:
            pmtwo_avg = str(pmtwo_avg)
        if pmten_avg == "":
            pmten_avg = "0"
        else:
            pmten_avg = str(pmten_avg)

        AqiQuality.objects.filter(sitename=site).update(county=county, aqi=aqi, pollutant=pollutant, status=status,
                                    pm10=pmten, pm25=pmtwo, wind_speed=wind_speed, wind_dict=wind_dic, pm10_avg=pmten_avg,
                                    pm25_avg=pmtwo_avg, longitude=longitude, latitude=latitude, date=date, time=time)


'''
        AqiQuality.objects.create(sitename=site, county=county, aqi=aqi, pollutant=pollutant, status=status,
                                  pm10=pmten, pm25=pmtwo, wind_speed=wind_speed, wind_dict=wind_dic, pm10_avg=pmten_avg,
                                  pm25_avg=pmtwo_avg, longitude=longitude, latitude=latitude, date=date, time=time)                                                       
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


aqi_crawler()