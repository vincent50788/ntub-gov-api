import json
import psycopg2
import requests


def insert():
    db_url = "postgres://kimbrxznkhibhy:cba6bae221b0fede1fff1d560ae0fc9bafa634ba31e6f3ca4c1239c6ea3438a1@ec2-184-72-237-95.compute-1.amazonaws.com:5432/d86jg6jbd1a4q6"
    con = psycopg2.connect(db_url)
    cur = con.cursor()
    url = "https://opendata.epa.gov.tw/webapi/Data/REWIQA/?$orderby=SiteName&$skip=0&$top=1000&format=json"
    re = requests.get(url, verify=False)
    js = json.loads(re.content)
    for a in js:
        site = a['SiteName']  # 測站名稱
        county = a['County']  # 地區
        aqi = (a['AQI'])
        status = a['Status']  # 品質狀態
        wind_speed = a['WindSpeed']  # 風速
        wind_dir = a['WindDirec']  # 風向
        publishtime = a['PublishTime']  # 發布時間
        longx = a['Longitude']
        laty = a['Latitude']

        if aqi == "":
            aqi = 0

        if wind_dir == "":
            wind_dir = 0

        if wind_speed == "":
            wind_speed = 0

        cur.execute('INSERT INTO weathers ("SiteName", "County", "AQI", "Status", "WindSpeed", "WindDir", "Date", "Time", "Longitude", "Latitude") '
                            'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);',(site, county, aqi, status, wind_speed, wind_dir, publishtime, publishtime, longx, laty))

    con.commit()
    cur.close()
    con.close()
    print('the end')



