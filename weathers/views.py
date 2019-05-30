from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import psycopg2

# Create your views here.


def get_data():  # 撈資料
    df = pd.DataFrame(columns=['SiteName', 'County', 'AQI', 'Status', 'WindSpeed', 'WindDir', 'Date', 'Time', 'Longitude', 'Latitude'])
    conn = psycopg2.connect("postgres://qavyefluuzpebh:705ea584327daef9b8f6ae4784b87625d13d99d8c681ce5a360286f75fe918f0@ec2-75-101-147-226.compute-1.amazonaws.com:5432/db7pcd9v2dl915")
    cur = conn.cursor()
    cur.execute("SELECT * FROM weathers")
    results = cur.fetchall()  # 搜取所有结果
    cur.close()
    conn.close()
    for a in results:
        site = a[0]  # 測站名稱
        county = a[1]  # 地區
        aqi = (a[2])
        status = a[3]  # 品質狀態
        wind_speed = a[4]  # 風速
        wind_dir = a[5]  # 風向
        date = a[6]  # 發布時間
        time = a[7]
        longx = a[8]
        laty = a[9]
        s = pd.Series([site, county, aqi, status, wind_speed, wind_dir, date, time, longx, laty],
                      index=['SiteName', 'County', 'AQI', 'Status', 'WindSpeed', 'WindDir', 'Date', 'Time', 'Longitude','Latitude'])
        df = df.append(s, ignore_index=True)
    data = df.to_html(index=False)
    return data


def weathers_request(request):
    return HttpResponse(get_data())


