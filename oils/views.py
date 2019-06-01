# from django.shortcuts import render
from django.http import HttpResponse
import psycopg2
import pandas as pd

# Create your views here.


def get_data():  # 從資料庫撈資料
    df = pd.DataFrame(columns=['92', '95', '98', '酒精汽油', '超級柴油', '液態瓦斯', 'Date', 'Time'])
    conn = psycopg2.connect("postgres://qavyefluuzpebh:705ea584327daef9b8f6ae4784b87625d13d99d8c681ce5a360286f75fe918f0@ec2-75-101-147-226.compute-1.amazonaws.com:5432/db7pcd9v2dl915")
    cur = conn.cursor()
    cur.execute("SELECT * FROM oils")
    results = cur.fetchall()  # 搜取所有结果
    cur.close()
    conn.close()
    for a in results:
        unleaded = a[1]
        super = a[2]
        supreme = a[3]
        alcohol_gas = a[4]
        diesel = a[5]
        liquefied_gas = a[6]
        date = a[7]
        time = a[8]

        s = pd.Series([unleaded, super, supreme, alcohol_gas, diesel, liquefied_gas, date, time],
                      index=['92', '95', '98', '酒精汽油', '超級柴油', '液態瓦斯', 'Date', 'Time'])
        df = df.append(s, ignore_index=True)
    data = df.to_html(index=False)
    return data


def oils_request(request):
    return HttpResponse(get_data())
