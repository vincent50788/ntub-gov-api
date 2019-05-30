from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd


# Create your views here.


def get_data():  # 撈資料
    df = pd.DataFrame(columns=['SiteName', 'County', 'AQI', 'Status', 'WindSpeed', 'WindDir', 'Date', 'Time', 'Longitude', 'Latitude'])
    conn = psycopg2.connect("postgres://kimbrxznkhibhy:cba6bae221b0fede1fff1d560ae0fc9bafa634ba31e6f3ca4c1239c6ea3438a1@ec2-184-72-237-95.compute-1.amazonaws.com:5432/d86jg6jbd1a4q6")
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
