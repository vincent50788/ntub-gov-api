from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import psycopg2

# Create your views here.

# 從資料庫撈資料
conn = psycopg2.connect( "postgres://qavyefluuzpebh:705ea584327daef9b8f6ae4784b87625d13d99d8c681ce5a360286f75fe918f0@ec2-75-101-147-226.compute-1.amazonaws.com:5432/db7pcd9v2dl915")
cur = conn.cursor()
cur.execute("SELECT * FROM dangerous_area")
results = cur.fetchall()  # 搜取所有结果
cur.close()
conn.close()


def get_method():
    df = pd.DataFrame(columns=['location', 'Longitude', 'Latitude'])
    for a in results:
        location = a[1]
        longitude = a[2]
        latitude = a[3]

        s = pd.Series([location, longitude, latitude],
                      index=['location', 'Longitude', 'Latitude'])
        df = df.append(s, ignore_index=True)
    data = df.to_html(index=False)
    return data


def post_method(user_long, user_lat):
    data_list = []
    hypotenuse_list = []  # 斜邊 list

    for a in results:
        a = list(a)

        long = float(a[2])
        lat = float(a[3])

        hypotenuse = (long-float(user_long))**2 + (lat-float(user_lat))**2
        hypotenuse_list.append(hypotenuse)
        a.append(hypotenuse)
        data_list.append(a)

    min_hy = min(hypotenuse_list)

    for b in data_list:  # 斜邊最小的 = List 最小斜邊
        if b[-1] == min_hy:
            s = pd.Series([b[1], b[2], b[3]], index=['location', 'Longitude', 'Latitude'])
            s = s.to_json(force_ascii=False)
        print(b)
    return s


def dangerousArea_request(request):  # http request

    if request.method == 'POST':
        user_long = request.POST.get("Longitude")
        user_lat = request.POST.get("Latitude")
        return HttpResponse(post_method(user_long, user_lat))
    else:
        return HttpResponse(get_method())


if __name__ == '__main__':
    post_method(0, 0)