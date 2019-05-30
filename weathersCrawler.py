import json
from weathers.models import Weathers
import requests


def insert():
    url = "https://opendata.epa.gov.tw/webapi/Data/REWIQA/?$orderby=SiteName&$skip=0&$top=1000&format=json"
    re = requests.get(url, verify=False)
    js = json.loads(re.content)
    for a in js:
        site_ = a['SiteName']  # 測站名稱
        county_ = a['County']  # 地區
        aqi_ = (a['AQI'])
        status_ = a['Status']  # 品質狀態
        windspeed_ = a['WindSpeed']  # 風速
        winddir_ = a['WindDirec']  # 風向
        date_ = a['PublishTime'].split(' ')[0]
        time_ = a['PublishTime'].split(' ')[1]
        longitude_ = a['Longitude']
        latitude_ = a['Latitude']

        if aqi_ == "":
            aqi_ = 0

        if winddir_ == "":
            winddir_ = 0

        if windspeed_ == "":
           windspeed_ = 0

        Weathers.objects.create(sitename=site_, county=county_, aqi=aqi_, status=status_, windspeed=windspeed_,
                                winddir=winddir_, date=date_, time=time_, longitude=longitude_, latitude=latitude_)

    print('the end')


insert()
