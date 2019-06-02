# topicbackground-NTUB
專題的後端，串接多個API or 網頁爬蟲， 再整理給前端iOS/Android。
## superCrawler.py
用來取得需要的資訊
## clock.py
定時執行superCrawler.py裡的function

## Heroku所需要的文檔
### requirements.txt 
下指令建立
> pip freeze > requirements.txt

### Procfile 
新增Procfile文字檔，不能有副檔名。       
web應用：
> web: gunicorn --pythonpath mysite mysite.wsgi  

定時執行.py：       
> clock: python clock.py


### production_settings.py
mysite/mysite/底下新增production_settings.py      
部署上去後，Heroku會使用這個production_settings.py
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
## Resource & DataBase
### weathers
> url = https://opendata.epa.gov.tw/webapi/Data/REWIQA/?$orderby=SiteName&$skip=0&$top=1000&format=json
> views = https://topic-ntub.herokuapp.com/weathers
### oils
> url = https://www.cpc.com.tw/Default.aspx  
> views = https://topic-ntub.herokuapp.com/oils/
### alerts
> url = https://opendata.cwb.gov.tw/fileapi/v1/opendataapi/W-C0033-001?Authorization=CWB-242E2AA6-F542-43E1-973D-9A0A4DBB7E5E&downloadType=WEB&format=JSON   
> views = https://topic-ntub.herokuapp.com/alerts/




