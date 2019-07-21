# from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import psycopg2


# Create your views here.

# 從資料庫撈資料
conn = psycopg2.connect( "postgres://qavyefluuzpebh:705ea584327daef9b8f6ae4784b87625d13d99d8c681ce5a360286f75fe918f0@ec2-75-101-147-226.compute-1.amazonaws.com:5432/db7pcd9v2dl915")
cur = conn.cursor()
cur.execute("SELECT * FROM aqi_quality")
results = cur.fetchall()  # 搜取所有结果
cur.close()
conn.close()


def get_method():
    df = pd.DataFrame(columns=['SiteName', 'County', 'AQI', 'Pollutant', 'Status', 'PM10', 'PM2.5', 'WindSpeed', 'WindDir',
                               'PM10_avg', 'PM2.5_avg', 'Longitude', 'Latitude', 'Date', 'Time'])
    for a in results:
        site = a[1]  # 測站名稱
        county = a[2]  # 地區
        aqi = a[3]
        pollutant = a[4]
        status = a[5]  # 品質狀態
        pmten = a[6]
        pmtwo = a[7]
        wind_speed = a[8]  # 風速
        wind_dic = a[9]  # 風向
        pmten_avg = a[10]
        pmtwo_avg = a[11]
        longitude = a[12]
        latitude = a[13]
        date = a[14]
        time = a[15]

        s = pd.Series([site, county, aqi, pollutant, status, pmten, pmtwo, wind_speed, wind_dic, pmten_avg, pmtwo_avg,
                       longitude, latitude, date, time],
                      index=['SiteName', 'County', 'AQI', 'Pollutant', 'Status', 'PM10', 'PM2.5', 'WindSpeed', 'WindDir',
                               'PM10_avg', 'PM2.5_avg', 'Longitude', 'Latitude', 'Date', 'Time'])
        df = df.append(s, ignore_index=True)
    data = df.to_html(index=False)
    return data


def post_method(user_long, user_lat):
    data_list = []
    hypotenuse_list = []

    for a in results:
        a = list(a)
        long = a[12]
        lat = a[13]
        hypotenuse = (long-user_long)**2 + (lat-user_lat)**2
        hypotenuse_list.append(hypotenuse)
        a.append(hypotenuse)
        data_list.append(a)

    min_hy = min(hypotenuse_list)

    for b in data_list:
        if b[-1] == min_hy:
            s = pd.Series([b[1], b[2], b[3], b[4], b[5], b[6], b[7], b[8], b[9], b[10], b[11], b[14], b[15]]
                          , index=['SiteName', 'County', 'AQI', 'Pollutant', 'Status', 'PM10', 'PM2.5', 'WindSpeed',
                                   'WindDir', 'PM10_avg', 'PM2.5_avg', 'Date', 'Time'])
            s = s.to_json(force_ascii=False)
            return s


def aqi_request(request):  # 傳前端
    if request.method == 'POST':
        user_long = request.POST.get('Longitude')
        user_lat = request.POST.get('Latitude')
        return HttpResponse(post_method(float(user_long), float(user_lat)))
    else:
        return HttpResponse(get_method())


