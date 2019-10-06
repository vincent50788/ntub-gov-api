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
from aqi_quality.views import aqi_request
from oils.views import oils_request
from alerts.views import alert_request
from weather.views import weather_request
from dangerous_area.views import dangerousArea_request

urlpatterns = [
    path('admin/', admin.site.urls),
    path('aqi/', aqi_request),
    path('oils/', oils_request),
    path('alerts/', alert_request),
    path('weather/', weather_request),
    path('dangerous/', dangerousArea_request)
]

