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
> Resource = https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/W-C0033-001?Authorization=CWB-242E2AA6-F542-43E1-973D-9A0A4DBB7E5E&downloadType=WEB&format=JSON   
> API = https://topic-ntub.herokuapp.com/warning/

#### AQI 
> Resource = https://opendata.epa.gov.tw/webapi/Data/REWIQA/?$orderby=SiteName&$skip=0&$top=1000&format=json 
> API = https://topic-ntub.herokuapp.com/aqi/

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
    "city": "基隆市",
    "warning": "",
    "date": "2019-10-08",
    "time": "19:31:00"
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
