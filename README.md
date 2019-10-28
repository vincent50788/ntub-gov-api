# topicbackground-NTUB
Background of Topic

## superCrawler.py
Web Crawler 

## clock.py


## Heroku所需要的文檔
### requirements.txt 
> pip freeze > requirements.txt

### Procfile 
Create Procfile
web App：
> web: gunicorn --pythonpath mysite mysite.wsgi  

clock.py：       
> clock: python clock.py


### production_settings.py
create production_settings.py for Heroku
mysite/mysite/production_settings.py 

```python
# Import all default settings.
from .settings import *

import dj_database_url
DATABASES = {
    'default': dj_database_url.config(),
}

# Static asset configuration.
STATIC_ROOT = 'staticfiles'

# Honor the 'X-Forwarded-Proto' header for request.is_secure().
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers.
ALLOWED_HOSTS = ['*']

# Turn off DEBUG mode.
DEBUG = False

```
## Resource & API
#### Weather Data
> Resource = https://opendata.epa.gov.tw/webapi/Data/REWIQA/?$orderby=SiteName&$skip=0&$top=1000&format=json  
> API = https://topic-ntub.herokuapp.com/weather/

#### Gas Price
> Resource = https://www.cpc.com.tw/Default.aspx  
> API = https://topic-ntub.herokuapp.com/gasprice/

#### Warning
> Resource = https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/O-A0003-001?Authorization=rdec-key-123-45678-011121314&format=JSON  
> API = https://topic-ntub.herokuapp.com/warning/

#### AQI 
> Resource = https://opendata.epa.gov.tw/webapi/Data/REWIQA/?$orderby=SiteName&$skip=0&$top=1000&format=json   
> API = https://topic-ntub.herokuapp.com/aqi/

#### PreWeather(天氣預測)
> Resource = https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/F-C0032-001?Authorization=rdec-key-123-45678-011121314&format=JSON  
> API = https://topic-ntub.herokuapp.com/preweather/

#### ParkNTPC(新北市停車格)
> Resource = https://data.ntpc.gov.tw/od/data/api/1A71BA9C-EF21-4524-B882-6D085DF2877A?$format=json  
> API = https://topic-ntub.herokuapp.com/partNTPC/

## Weather(天氣)
request : 
```json
{
    "Longitude": " ",
    "Latitude": " "
}
```
response :
```json
{
    "result": 1,
    "locationName": " ",
    "windDir": " ",
    "windSpeed": " ",
    "tempNow": " ",
    "humidity": " ",
    "rainFall": " ",
    "uviH": " ",
    "uviStatus": " ",
    "tempMax": " ",
    "tempMaxTime": " ",
    "tempMin": " ",
    "tempMinTime": " "
}
```


## AQI(空氣品質)
request : 
```json
{
    "Longitude": " ",
    "Latitude": " "
}
```
response :
```json
{
    "result": 1,
    "SiteName": " ",
    "County": " ",
    "AQI": " ",
    "Pollutant": "",
    "AQIStatus": " ",
    "PM10": " ",
    "PM2.5": " ",
    "WindSpeed": " ",
    "WindDir": " ",
    "PM10Avg": " ",
    "PM2.5Avg": " ",
    "Date": " ",
    "Time": " ",
    "PM2.5Status": " ",
    "So2": " ",
    "Co": " ",
    "O3": " ",
    "So2Avg": " "
}
```


## Warning(警報)
request : 
```json
{
    "Longitude": " ",
    "Latitude": " "
}
```
response :
```json
{
    "result": 1,
    "city": "",
    "warning": "",
    "date": "",
    "time": ""
}
```


## GasPrice(油價)
request : 
```json
{
    "GetPrice": 1
}
```
response :
```json
{
    "result": 1,
    "unleaded": "26.3",
    "super_": "27.8",
    "supreme": "29.8",
    "alcoholGas": "27.8",
    "diesel": "24.1",
    "liquefiedGas": "16.6"
}
```


## PreWeather(天氣預測)  
> 近36小時天氣預報  
request : 
```json
{
    "Longitude": " ",
    "Latitude": " "
}
```
response :
```json
{
    "result": 1,
    "city": "連江縣",
    "NowStartDate": "2019-10-19", //預測開始時間
    "NowStartTime": "12:00:00", 
    "NowEndDate": "2019-10-19",//預測結束時間
    "NowEndTime": "18:00:00",
    "NowMaxT": "24", //最高溫
    "NowMinT": "22", //最低溫
    "NowPoP": "0",  //降雨機率
    "NowWx": "晴時多雲",  //天氣描述
    "CloseStartDate": "2019-10-19",
    "CloseStartTime": "18:00:00",
    "CloseEndDate": "2019-10-20",
    "CloseEndTime": "06:00:00",
    "CloseMaxT": "22",
    "CloseMinT": "21",
    "ClosePoP": "0",
    "CloseWx": "晴時多雲",
    "FarStartDate": "2019-10-20",
    "FarStartTime": "06:00:00",
    "FarEndDate": "2019-10-20",
    "FarEndTime": "18:00:00",
    "FarMaxT": "24",
    "FarMinT": "21",
    "FarPoP": "0",
    "FarWx": "晴時多雲"
}
```


## ParkNTPC(新北市汽車停車格)

| contain | type |reponse  |
|:--------:|:----:|:-----|
| "0"     |  "0" | 所有車位 |
| "0"     |  "1" | 所有空車位("不包含"非收費時段 時段性禁停)  |
| "0"     |  "2" | 所有空車位("包含"非收費時段 時段性禁停)    |
| "1"     |  "0" | 自己最近的一個車位   |
| "1"     |  "1" | 自己最近的一個空車位("不包含"非收費時段 時段性禁停)   |
| "1"     |  "2" | 自己最近的一個空車位("包含"非收費時段 時段性禁停)   |
| "1"     |  "3" | 自己500m所有車位   |
| "1"     |  "4" | 自己500m的所有空車位("不包含"非收費時段 時段性禁停)   |
| "1"     |  "5" | 自己500m的所有空車位("包含"非收費時段 時段性禁停)   |
| "1"     |  "6" | 自己1000m所有車位   |
| "1"     |  "7" | 自己1000m的所有空車位("不包含"非收費時段 時段性禁停)   |
| "1"     |  "8" | 自己1000m的所有空車位("包含"非收費時段 時段性禁停)  |
| "1"     |  "9" | 自己1500m所有車位   |
| "1"     |  "10" | 自己500m的所有空車位("不包含"非收費時段 時段性禁停)   |
| "1"     |  "11" | 自己500m的所有空車位("包含"非收費時段 時段性禁停)   |


request : 
```json
{
    "Longitude": 120,
    "Latitude": 25,
    "contain": "1" ,
    "type": "2" 
}

```
response :
```json
{
    "result": 1,
    "type": "離自己最近的一個空車位(包含 非收費時段 時段性禁停)",
    "parks": [
        {
            "NAME": "汽車停車位",
            "DAY": "週一-週五",
            "HOUR": "08:00-18:00",
            "PAY": "限時計次收",
            "PAYCASH": "每次四小時30元/次",
            "MEMO": null,
            "CellStatus": "N",
            "IsNowCash": "false", //此時是否收費
            "ParkStatus": "3",
            "ParkStatusZh": "非收費時段",
            "Haversine": "136836.2325606173", //距離(非實際距離)
            "Longitude": "121.3561234829446",
            "Latitude": "25.06795831535265"
        }
    ]
}
```
