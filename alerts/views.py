# from django.shortcuts import render
import psycopg2
import pandas as pd
from django.http import HttpResponse
# Create your views here.

# Connect DB
conn = psycopg2.connect("postgres://qavyefluuzpebh:705ea584327daef9b8f6ae4784b87625d13d99d8c681ce5a360286f75fe918f0@ec2-75-101-147-226.compute-1.amazonaws.com:5432/db7pcd9v2dl915")
cur = conn.cursor()
cur.execute("SELECT * FROM alerts")
results = cur.fetchall()
cur.close()
conn.close()


def post_method(user_long, user_lat):
    data_list = []
    hypotenuse_list = []

    for a in results:
        a = list(a)  # 轉成List
        long = float(a[4])
        lat = float(a[5])
        hypotenuse = (long-float(user_long))**2 + (lat-float(user_lat))**2
        hypotenuse_list.append(hypotenuse)
        a.append(hypotenuse)
        data_list.append(a)

    min_hy = min(hypotenuse_list)  # 取最小的斜邊

    for b in data_list:
        if b[-1] == min_hy:
            s = pd.Series([b[0], b[1], b[2], b[3]]
                          , index=['city', 'hazard', 'date', 'time'])
            s = s.to_json(force_ascii=False)
            return s


def get_method():
    df = pd.DataFrame(columns=['city', 'hazard', 'date', 'time'])
    for a in results:
        city = str(a[0])
        hazard = str(a[1])
        date = str(a[2])
        time = str(a[3])
        s = pd.Series([city, hazard, date, time], index=['city', 'hazard', 'date', 'time'])
        df = df.append(s, ignore_index=True)
    data = df.to_json(orient='index')
    return data


def alert_request(request):
    if request.method == 'POST':
        user_long = request.POST.get('Longitude')
        user_lat = request.POST.get('Latitude')
        return HttpResponse(post_method(user_long, user_lat), content_type='application/json')
    else:
        return HttpResponse(get_method())

