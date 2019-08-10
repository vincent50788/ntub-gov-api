# 單獨執行.pyError
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "topic_crawler.settings")

import django
django.setup()
# package
import json
import requests
from datetime import datetime, timedelta
import pyproj
# DB
from aqi_quality.models import AqiQuality
from oils.models import Oils
from alerts.models import Alerts
from weather.models import Weather

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

        sotwo = a['SO2']
        co = a['CO']
        othree = a['O3']
        sotwo_avg = a['SO2_AVG']

        if aqi == "":
            aqi = "0"
        else:
            aqi = str(aqi)

        if pmten == "":
            pmten = "0"
        else:
            pmten = str(pmten)

        if pmtwo == "" or pmtwo == "ND":
            pmtwo = "0"
        else:
            pmtwo = str(pmtwo)

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

        if sotwo == "":
            sotwo = "0"
        else:
            sotwo = str(sotwo)

        if co == "":
            co = "0"
        else:
            co = str(co)

        if othree == "":
            othree = "0"
        else:
            othree = str(othree)

        if sotwo_avg == "":
            sotwo_avg = "0"
        else:
            sotwo_avg = str(sotwo_avg)

        if float(pmtwo) > 0 and float(pmtwo) <= 15.5:
            pmtwo_status = "良好"
        elif float(pmtwo) > 15.5 and float(pmtwo) <= 35.5:
            pmtwo_status = "普通"
        elif float(pmtwo) > 35.5 and float(pmtwo) <= 54.5:
            pmtwo_status = "對敏感族群不健康"
        elif float(pmtwo) > 54.5 and float(pmtwo) <= 150.5:
            pmtwo_status = "不健康"
        elif float(pmtwo) > 150.5 and float(pmtwo) >= 250.5:
            pmtwo_status = "非常不健康"
        elif float(pmtwo) > 250.5:
            pmtwo_status = "危險"
        else:
            pmtwo_status = "設備維護"

        AqiQuality.objects.filter(sitename=site).update(county=county, aqi=aqi, pollutant=pollutant, status=status,
                                    pm10=pmten, pm25=pmtwo, wind_speed=wind_speed, wind_dict=wind_dic, pm10_avg=pmten_avg,
                                    pm25_avg=pmtwo_avg, longitude=longitude, latitude=latitude, date=date, time=time,
                                    pmtwo_status=pmtwo_status, sotwo=sotwo, co=co, othree=othree, sotwo_avg=sotwo_avg)


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


def weather_crawler():
    url = "https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/O-A0003-001?Authorization=rdec-key-123-45678-011121314&format=JSON"
    re = requests.get(url, verify=False)
    js = json.loads(re.content)
    data = js['cwbopendata']['location']
    wdir, wdsd, temp, humd, rainfall, uvi_h, temp_max, tmax＿time, temp_min, tmin_time = "", "", "", "", "", "", "", "", "", ""
    for a in data:
        lon = str(a['lon'])  # 經緯度
        lat = str(a['lat'])
        locationName = a['locationName']  # 測站名稱
        time = a['time']
        weather_element = a['weatherElement']  # 天氣 Array
        for b in weather_element:
            if b['elementName'] == 'WDIR':  # 風向
                wdir = str(b['elementValue']['value'])
                if wdir == "-99":
                    wdir = "保養中"

            if b['elementName'] == 'WDSD':  # 風速
                wdsd = str(b['elementValue']['value'])
                if wdsd == "-99":
                    wdsd = "保養中"
            if b['elementName'] == 'TEMP':  # 溫度
                temp = str(b['elementValue']['value'])
                if temp == "-99":
                    temp = "保養中"

            if b['elementName'] == 'HUMD':  # 濕度
                humd = b['elementValue']['value']
                if humd == "-99":
                    humd = "保養中"

            if b['elementName'] == '24R':  # 累積雨量
                rainfall = b['elementValue']['value']
                if rainfall == "-99":
                    rainfall = "保養中"
            if b['elementName'] == 'H_UVI':  # 小時紫外線
                uvi_h = b['elementValue']['value']
                if uvi_h == "-99":
                    uvi_h = "保養中"
                    uvi_status = "保養中"
                else:
                    if float(uvi_h) > 0 and float(uvi_h) <= 2:
                        uvi_status = "低量級"
                    elif float(uvi_h) > 2 and float(uvi_h) <= 5:
                        uvi_status = "中量級"
                    elif float(uvi_h) > 5 and float(uvi_h) <= 7:
                        uvi_status = "高量級"
                    elif float(uvi_h) > 7 and float(uvi_h) <= 10:
                        uvi_status = "過量級"
                    else:
                        uvi_status = "危險級"

            if b['elementName'] == 'D_TX':  # 最高溫度
                temp_max = b['elementValue']['value']
                if temp_max == "-99":
                    temp_max = "保養中"

            if b['elementName'] == 'D_TXT':  # 最高溫度發生時間
                tmax＿time = b['elementValue']['value']
                if tmax＿time == "-99":
                    tmax＿time = "保養中"

            if b['elementName'] == 'D_TN':  # 最低溫
                temp_min = b['elementValue']['value']
                if temp_min == "-99":
                    temp_min = "保養中"

            if b['elementName'] == 'D_TNT':  # 最低溫發生時間
                tmin_time = b['elementValue']['value']
                if tmin_time == "-99":
                    tmin_time = "保養中"


        Weather.objects.filter(locationname=locationName).update(longitude=lon, latitude=lat, wind_dir=wdir, wind_speed=wdsd,
                               temp_now=temp, humd=humd, rainfall=rainfall, h_uvi=uvi_h, temp_max=temp_max,
                               tmax_time=tmax＿time, temp_min=temp_min, tmin_time=tmin_time, uvi_status=uvi_status)
        '''
        Weather.objects.create(locationname=locationName, longitude=lon, latitude=lat, wind_dir=wdir, wind_speed=wdsd,
                               temp_now=temp, humd=humd, rainfall=rainfall, h_uvi=uvi_h, temp_max=temp_max,
                               tmax_time=tmax＿time, temp_min=temp_min, tmin_time=tmin_time)
        '''


