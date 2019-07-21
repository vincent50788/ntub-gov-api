# from django.shortcuts import render
import psycopg2
import pandas as pd
from django.http import HttpResponse
# Create your views here.

# 連到資料庫
conn = psycopg2.connect("postgres://qavyefluuzpebh:705ea584327daef9b8f6ae4784b87625d13d99d8c681ce5a360286f75fe918f0@ec2-75-101-147-226.compute-1.amazonaws.com:5432/db7pcd9v2dl915")
cur = conn.cursor()
cur.execute("SELECT * FROM alerts")
results = cur.fetchall()  # 搜取所有資料
cur.close()
conn.close()


def post_alert(location):
    for a in range(0, len(results)):
        if location == results[a][0]:
            hazard = results[a][1]
            if hazard == "":
                hazard = "風平浪靜"
            return hazard


def get_data():
    df = pd.DataFrame(columns=['city', 'hazard', 'Date', 'Time'])
    for a in results:
        city = str(a[0])
        hazard = str(a[1])
        date = str(a[2])
        time = str(a[3])
        s = pd.Series([city, hazard, date, time], index=['city', 'hazard', 'Date', 'Time'])
        df = df.append(s, ignore_index=True)
    data = df.to_json(orient='index')
    print(data)
    return data


def alert_request(request):
    if request.method == 'POST':
        userCity = request.POST.get('city')
        userHazard = post_alert(userCity)
        s = pd.Series([userHazard], index=["hazard"])
        s = s.to_json(force_ascii=False)
        return HttpResponse(s)
    else:
        return HttpResponse(get_data())


