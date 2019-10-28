# from django.shortcuts import render
from django.http import JsonResponse
from ntubtopic.models import *
import json

# Create your views here.


def PostAqiQuality(request):
    result = {'result': 0}
    db_locations = AqiQuality.objects.all()
    data = json.loads(request.body.decode(encoding="utf-8"))
    hypotenuse_list = []
    user_long = data['Longitude']
    user_lat = data['Latitude']

    for a in db_locations:
        db_long = a.longitude
        db_lat = a.latitude
        hypotenuse = (float(db_long) - float(user_long)) ** 2 + (float(db_lat) - float(user_lat)) ** 2
        hypotenuse_list.append(hypotenuse)

    min_hypotenuse = min(hypotenuse_list)

    try:
        for b in db_locations:
            if min_hypotenuse == (float(b.longitude) - float(user_long)) ** 2 + (float(b.latitude) - float(user_lat)) ** 2:
                result['result'] = 1
                result['SiteName'] = b.sitename
                result['County'] = b.county
                result['AQI'] = b.aqi
                result['Pollutant'] = b.pollutant
                result['AQIStatus'] = b.status
                result['PM10'] = b.pm10
                result['PM2.5'] = b.pm25
                result['WindSpeed'] = b.wind_speed
                result['WindDir'] = b.wind_dict
                result['PM10Avg'] = b.pm10_avg
                result['PM2.5Avg'] = b.pm25_avg
                result['Date'] = b.date
                result['Time'] = b.time
                result['PM2.5Status'] = b.pmtwo_status
                result['So2'] = b.sotwo
                result['Co'] = b.co
                result['O3'] = b.othree
                result['So2Avg'] = b.sotwo_avg
    except Exception as e:
        result['error'] = str(e)

    return JsonResponse(result)
