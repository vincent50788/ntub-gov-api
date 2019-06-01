# from django.shortcuts import render
import psycopg2
import pandas as pd
from django.http import HttpResponse
# Create your views here.


def get_data():  # 從資料庫撈資料
    df = pd.DataFrame(columns=['city', 'hazard', 'affectedArea', 'phenomena', 'Date', 'Time'])
    conn = psycopg2.connect("postgres://qavyefluuzpebh:705ea584327daef9b8f6ae4784b87625d13d99d8c681ce5a360286f75fe918f0@ec2-75-101-147-226.compute-1.amazonaws.com:5432/db7pcd9v2dl915")
    cur = conn.cursor()
    cur.execute("SELECT * FROM alerts")
    results = cur.fetchall()  # 搜取所有结果
    cur.close()
    conn.close()
    for a in results:
        city = a[0]
        hazard = a[1]
        affectedareas = a[2]
        phenomena = a[3]
        date = a[4]
        time = a[5]

        s = pd.Series([city, hazard, affectedareas, phenomena, date, time],
                      index=['city', 'hazard', 'affectedArea', 'phenomena', 'Date', 'Time'])
        df = df.append(s, ignore_index=True)
    data = df.to_html(index=False)
    return data


def alert_request(request):
    return HttpResponse(get_data())


get_data()