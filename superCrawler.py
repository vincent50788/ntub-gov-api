# settings
import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "topic_crawler.settings")
django.setup()

# package
import json
import requests
from datetime import datetime, timedelta
import base64
from wsgiref.handlers import format_date_time
from hashlib import sha1
import hmac
from time import mktime

# Table
from ntubtopic.models import *

dateTime_ = datetime.now() + timedelta(hours=8)
theTime = dateTime_.strftime('%H:%M')
theDate = dateTime_.strftime('%Y-%m-%d')

app_id = '9485a3d80a6d49ff88239e525bcd8952'
app_key = 'IZu2bla9851Pv7K9jZ9Jldwikmw'


class Auth():

    def __init__(self, app_id, app_key):
        self.app_id = app_id
        self.app_key = app_key

    def get_auth_header(self):
        xdate = format_date_time(mktime(datetime.now().timetuple()))
        hashed = hmac.new(self.app_key.encode('utf8'), ('x-date: ' + xdate).encode('utf8'), sha1)
        signature = base64.b64encode(hashed.digest()).decode()

        authorization = 'hmac username="' + self.app_id + '", ' + \
                        'algorithm="hmac-sha1", ' + \
                        'headers="x-date", ' + \
                        'signature="' + signature + '"'
        return {
            'Authorization': authorization,
            'x-date': format_date_time(mktime(datetime.now().timetuple())),
            'Accept - Encoding': 'gzip'
        }


def spl(value):  # split date & time
    value = value.split(".", 1)[0]
    date = value[0:10]
    time = value[11:16]
    timeList = [date, time]
    return timeList


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
        print(locationName, hazard)
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
        # time = a['time']
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
                    if float(uvi_h) >= 0 and float(uvi_h) <= 2:
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


def dangerous_area():
    # https://data.gov.tw/dataset/6247
    url = "https://od.moi.gov.tw/api/v1/rest/datastore/A01010000C-000628-039"
    re = requests.get(url)
    js = json.loads(re.content)
    data = js['result']['records']
    for a in data:
        adress = a['Address']
        # DangerousArea.objects.create(location=adress)


def pre_weather():
    url = "https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/F-C0032-001?Authorization=rdec-key-123-45678-011121314&format=JSON"
    re = requests.get(url, verify=False)
    js = json.loads(re.content)
    data_set = js['cwbopendata']["dataset"]["location"]


    for data in data_set:
        location = data['locationName']
        weather_element = data['weatherElement']

        elements = weather_element[0]
        times = elements['time']

        # -----

        wx_today_time = times[0]
        today_startTime = spl(wx_today_time['startTime'])[1]
        today_startDate = spl(wx_today_time['startTime'])[0]
        today_endTime = spl(wx_today_time['endTime'])[1]
        today_endDate = spl(wx_today_time['endTime'])[0]
        today_wx = wx_today_time['parameter']['parameterName']

        wx_today_time_ = times[1]
        today_startDate_ = spl(wx_today_time_['startTime'])[0]
        today_endDate_ = spl(wx_today_time_['endTime'])[0]
        today_startTime_ = spl(wx_today_time_['startTime'])[1]
        today_endTime_ = spl(wx_today_time_['endTime'])[1]
        today_wx_ = wx_today_time_['parameter']['parameterName']

        wx_tomorrow_time = times[2]
        tomorrow_startTime = spl(wx_tomorrow_time['startTime'])[1]
        tomorrow_endTime = spl(wx_tomorrow_time['endTime'])[1]
        tomorrow_startDate = spl(wx_tomorrow_time['startTime'])[0]
        tomorrow_endDate = spl(wx_tomorrow_time['endTime'])[0]
        tomorrow_wx = wx_tomorrow_time['parameter']['parameterName']


        maxT_elements = weather_element[1]
        maxT_times = maxT_elements['time']

        maxT_today_time = maxT_times[0]
        today_maxT = maxT_today_time['parameter']['parameterName']

        maxT_today_time_ = maxT_times[1]
        today_maxT_ = maxT_today_time_['parameter']['parameterName']

        maxT_tomorrow_time = maxT_times[2]
        tomorrow_maxT = maxT_tomorrow_time['parameter']['parameterName']

        # -----

        minT_elements = weather_element[2]
        minT_times = minT_elements['time']

        minT_today_time = minT_times[0]
        today_minT = minT_today_time['parameter']['parameterName']

        minT_today_time_= minT_times[1]
        today_minT_ = minT_today_time_['parameter']['parameterName']

        minT_tomorrow_time = minT_times[2]
        tomorrow_minT = minT_tomorrow_time['parameter']['parameterName']

        # -----

        pop_elements = weather_element[4]
        pop_times = pop_elements['time']

        pop_today_time = pop_times[0]
        today_pop = pop_today_time['parameter']['parameterName']

        pop_today_time_ = pop_times[1]
        today_pop_ = pop_today_time_['parameter']['parameterName']

        pop_tomorrow_time = pop_times[2]
        tomorrow_pop = pop_tomorrow_time['parameter']['parameterName']

        '''
        PreWeather.objects.create(city=location, today_starttime=today_startTime, today_startdate=today_startDate, today_endtime=today_endTime,
                                  today_enddate=today_endDate, today_starttime_field=today_startTime_, today_startdate_field=today_startDate,
                                  today_endtime_field=today_endTime_, today_enddate_field=today_endDate_, tomorrow_startdate=tomorrow_startDate,
                                  tomorrow_starttime=tomorrow_startTime, tomorrow_enddate=tomorrow_endDate, tomorrow_endtime=tomorrow_endTime,
                                  )
        '''

        PreWeather.objects.filter(city=location).update(today_starttime=today_startTime, today_startdate=today_startDate, today_endtime=today_endTime,
                                  today_enddate=today_endDate, today_starttime_field=today_startTime_, today_startdate_field=today_startDate,
                                  today_endtime_field=today_endTime_, today_enddate_field=today_endDate_, tomorrow_startdate=tomorrow_startDate,
                                  tomorrow_starttime=tomorrow_startTime, tomorrow_enddate=tomorrow_endDate, tomorrow_endtime=tomorrow_endTime,
                                  today_maxt=today_maxT, today_maxt_field=today_maxT_, tomorrow_maxt=tomorrow_maxT, today_mint=today_minT,
                                  today_mint_field=today_minT_, tomorrow_mint=tomorrow_minT, today_wx=today_wx, today_wx_field=today_wx_,
                                  tomorrow_wx=tomorrow_wx, today_pop=today_pop, today_pop_field=today_pop_, tomorrow_pop =tomorrow_pop)


def parting_ntpc():
    url = "https://data.ntpc.gov.tw/od/data/api/1A71BA9C-EF21-4524-B882-6D085DF2877A?$format=json"
    re = requests.get(url, verify=False)
    partslist = []
    js = json.loads(re.content)

    for data in js:
        name = data['NAME']  # 車格類型
        day = data['DAY']  # 收費天
        hour = data['HOUR']  # 收費時段
        pay = data['PAY']
        cash = data['PAYCASH']
        memo = data['MEMO']
        status = data['CELLSTATUS']  # 車格狀態判斷 T/F
        cashStatus = data['ISNOWCASH']
        parkingStatus = data['ParkingStatus']
        if parkingStatus == "1":
            parkingStatusZh = "有車"
        elif parkingStatus == "2":
            parkingStatusZh = "空位"
        elif parkingStatus == "3":
            parkingStatusZh = "非收費時段"
        elif parkingStatus == "4":
            parkingStatusZh = "時段性禁停"
        else:
            parkingStatusZh = "尚無資訊"

        lon = data['lon']
        lat = data['lat']

        partdic = {'NAME': name, 'DAY': day, 'HOUR': hour, 'PAY': pay, 'CASH': cash, 'MEMO': memo, 'IsNowCash': cashStatus,
                   'Status': status, 'ParkingStatus': parkingStatus, 'ParkStatusZh': parkingStatusZh, 'Longitude': lon,
                   'Latitude': lat}
        partslist.append(partdic)

    return partslist


def bike_crawler():
    au = Auth(app_id, app_key)

    urls_id = ["https://ptx.transportdata.tw/MOTC/v2/Bike/Station/Taipei?$format=JSON",  # 台北
               "https://ptx.transportdata.tw/MOTC/v2/Bike/Station/NewTaipei?$format=JSON",
               "https://ptx.transportdata.tw/MOTC/v2/Bike/Station/Hsinchu?$format=JSON",
                "https://ptx.transportdata.tw/MOTC/v2/Bike/Station/MiaoliCounty?$format=JSON",
               "https://ptx.transportdata.tw/MOTC/v2/Bike/Station/ChanghuaCounty?$format=JSON",
               "https://ptx.transportdata.tw/MOTC/v2/Bike/Station/PingtungCounty?$format=JSON",
               "https://ptx.transportdata.tw/MOTC/v2/Bike/Station/Taoyuan?$format=JSON",
               "https://ptx.transportdata.tw/MOTC/v2/Bike/Station/Kaohsiung?$format=JSON",
               "https://ptx.transportdata.tw/MOTC/v2/Bike/Station/Tainan?$format=JSON",
               "https://ptx.transportdata.tw/MOTC/v2/Bike/Station/Taichung?$format=JSON"
    ]

    urls_bike = ["https://ptx.transportdata.tw/MOTC/v2/Bike/Availability/Taipei?$format=JSON",
                 "https://ptx.transportdata.tw/MOTC/v2/Bike/Availability/NewTaipei?$format=JSON",
                 "https://ptx.transportdata.tw/MOTC/v2/Bike/Availability/Hsinchu?$format=JSON",
                 "https://ptx.transportdata.tw/MOTC/v2/Bike/Availability/MiaoliCounty?$format=JSON",
                 "https://ptx.transportdata.tw/MOTC/v2/Bike/Availability/ChanghuaCounty?$format=JSON",
                 "https://ptx.transportdata.tw/MOTC/v2/Bike/Availability/PingtungCounty?$format=JSON",
                 "https://ptx.transportdata.tw/MOTC/v2/Bike/Availability/Taoyuan?$format=JSON",
                 "https://ptx.transportdata.tw/MOTC/v2/Bike/Availability/Kaohsiung?$format=JSON",
                 "https://ptx.transportdata.tw/MOTC/v2/Bike/Availability/Tainan?$format=JSON",
                 "https://ptx.transportdata.tw/MOTC/v2/Bike/Availability/Taichung?$format=JSON"

    ]

    # https://ptx.transportdata.tw/MOTC?t=Bike&v=2#!/Bike/BikeApi_Availability
    bikeList = []

    for a in range(len(urls_bike)):
    # get id
        url_id = urls_id[a]
        re_id = requests.get(url_id, headers=au.get_auth_header())
        js_id = json.loads(re_id.content)

        # get available bike
        url_bike = urls_bike[a]
        re_bike = requests.get(url_bike, headers=au.get_auth_header())
        js_bike = json.loads(re_bike.content)

        for a in js_id:
            for b in js_bike:

                if a['StationUID'] == b['StationUID']:
                    stationUID = a['StationUID']
                    stationID = a['StationID']
                    stationName_zh = a['StationName']['Zh_tw']
                    # stationName_en = a['StationName']['En']
                    stationLatitude = a['StationPosition']['PositionLat']
                    stationLongitude = a['StationPosition']['PositionLon']
                    stationAddress_zh = a['StationAddress']['Zh_tw']
                    # stationAddress_en = a['StationAddress']['En']
                    bikesCapacity = a['BikesCapacity']
                    servieAvailable = b['ServieAvailable']  # 服務狀態:[0:'停止營運',1:'正常營運']
                    availableRentBikes = b['AvailableRentBikes']  # 可租借個數
                    availableReturnBikes = b['AvailableReturnBikes']  # 可歸還數
                    updateTime = a['UpdateTime']
            bikedic = {'StationUID': stationUID, 'StationID': stationID, 'StationName_zh': stationName_zh, 'StationLatitude': stationLatitude,
                       'StationLongitude': stationLongitude, 'stationAddress_zh': stationAddress_zh, 'BikesCapacity': bikesCapacity,
                       'ServieAvailable': servieAvailable, 'AvailableRentBikes': availableRentBikes, 'AvailableReturnBikes': availableReturnBikes,
                       'UpdateTime': updateTime}
            bikeList.append(bikedic)

    return bikeList


def scenicSpot_crawler():  # 觀光景點
    a = Auth(app_id, app_key)

    # https://ptx.transportdata.tw/MOTC?t=Tourism&v=2#!/Tourism/TourismApi_ScenicSpot
    scenicList = []
    # get id
    url_id = "https://ptx.transportdata.tw/MOTC/v2/Tourism/ScenicSpot?$format=JSON"
    re_id = requests.get(url_id, headers=a.get_auth_header())
    js_id = json.loads(re_id.content)

    for a in js_id:
        scenicName = a["Name"]
        scenicAdress = a.get("Address", "none")
        scenicDescription = a.get("Description", "none")
        scenicLongitude = a["Position"]["PositionLon"]
        scenicLatitude = a["Position"]["PositionLat"]
        scenicPhone = a.get("Phone", "none")
        scenicOpentime = a.get("OpenTime", "none")

        scenicDic = {'ScenicName': scenicName, 'ScenicAddress': scenicAdress, 'ScenicDescription': scenicDescription, 'ScenicLongitude': scenicLongitude,
                     'ScenicLatitude': scenicLatitude, 'ScenicPhone': scenicPhone, 'ScenicOpentime': scenicOpentime}
        scenicList.append(scenicDic)
    return scenicList


bike_crawler()