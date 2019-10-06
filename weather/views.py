from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import json
import psycopg2

# Create your views here.

# Connect DB
conn = psycopg2.connect( "postgres://qavyefluuzpebh:705ea584327daef9b8f6ae4784b87625d13d99d8c681ce5a360286f75fe918f0@ec2-75-101-147-226.compute-1.amazonaws.com:5432/db7pcd9v2dl915")
cur = conn.cursor()
cur.execute("SELECT * FROM weather")
results = cur.fetchall()  # search data
cur.close()
conn.close()


def get_method():
    df = pd.DataFrame(columns=['locationName', 'Longitude', 'Latitude', 'Wind_dir', 'Wind_speed', 'temp_now', 'humd', 'RainFall', 'UVI_H',
                               'temp_max', 'tmax_time', 'temp_min', 'tmin_time', 'uvi_status'])
    for a in results:
        location = a[0]  # siteName
        longitude = a[1]
        latitude = a[2]
        wind_dir = a[3]
        wind_speed = a[4]
        temp_now = a[5]
        humd = a[6]
        rainfall = a[7]
        uvi_h = a[8]
        temp_max = a[9]
        tmax_time = a[10]
        temp_min = a[11]
        tmin_time = a[12]
        uvi_status = a[14]

        s = pd.Series([location, longitude, latitude, wind_dir, wind_speed, temp_now, humd, rainfall, uvi_h, temp_max,
                       tmax_time, temp_min, tmin_time, uvi_status],
                      index=['locationName', 'Longitude', 'Latitude', 'Wind_dir', 'Wind_speed', 'temp_now', 'humd', 'RainFall', 'UVI_H',
                               'temp_max', 'tmax_time', 'temp_min', 'tmin_time', 'uvi_status'])
        df = df.append(s, ignore_index=True)
    data = df.to_html(index=False)

    return data


def post_method(user_long, user_lat):
    data_list = []
    hypotenuse_list = []  # 斜邊 list

    for a in results:
        a = list(a)
        long = float(a[1])
        lat = float(a[2])
        hypotenuse = (long-float(user_long))**2 + (lat-float(user_lat))**2
        hypotenuse_list.append(hypotenuse)
        a.append(hypotenuse)
        data_list.append(a)

    min_hy = min(hypotenuse_list)

    for b in data_list:
        if b[-1] == min_hy:
            s = pd.Series([b[0], b[1], b[2], b[3], b[4], b[5], b[6], b[7], b[8], b[9], b[10], b[11], b[12], b[14]]
                          , index=['locationName', 'Longitude', 'Latitude', 'Wind_dir', 'Wind_speed', 'temp_now', 'humd', 'RainFall', 'UVI_H',
                               'temp_max', 'tmax_time', 'temp_min', 'tmin_time', 'uvi_status'])
            s = s.to_json(force_ascii=False)
    return s


def weather_request(request):  # http request

    if request.method == 'POST':
        user_long = request.POST.get("Longitude")
        user_lat = request.POST.get("Latitude")
        return HttpResponse(post_method(user_long, user_lat))
    else:
        return HttpResponse(get_method())

