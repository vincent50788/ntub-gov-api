"""topic_crawler URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from ntubtopic.views import views_gas_price
from ntubtopic.views import views_air_quality
from ntubtopic.views import views_weather
from ntubtopic.views import views_environmental_warning
from ntubtopic.views import views_pre_weather
from ntubtopic.views import views_partingNTPC
from ntubtopic.views import views_bike

urlpatterns = [
    path('admin/', admin.site.urls),
    path('gasprice/', views_gas_price.PostOilPrice),
    path('aqi/', views_air_quality.PostAqiQuality),
    path('weather/', views_weather.PostWeather),
    path('warning/', views_environmental_warning.PostEnvironmentalWarning),
    path('preweather/', views_pre_weather.PostPreWeather),
    path('parkNTPC/', views_partingNTPC.PostNTPCPart),
    path('getAllBike/', views_bike.get_all_bikes),
    path('getCloseBike/', views_bike.get_close_bike)
]

