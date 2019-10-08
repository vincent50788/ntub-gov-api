# from django.shortcuts import render
from django.http import JsonResponse
from ntubtopic.models import *
import json


def PostWeather(request):
    result = {'result': 0}
    db_locations = Weather.objects.all()
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
                result['locationName'] = b.locationname
                result['windDir'] = b.wind_dir
                result['windSpeed'] = b.wind_speed
                result['tempNow'] = b.temp_now
                result['humidity'] = b.humd
                result['rainFall'] = b.rainfall
                result['uviH'] = b.h_uvi
                result['uviStatus'] = b.uvi_status
                result['tempMax'] = b.temp_max
                result['tempMaxTime'] = b.tmax_time
                result['tempMin'] = b.temp_min
                result['tempMinTime'] = b.tmin_time

    except Exception as e:
        result['error'] = str(e)

    return JsonResponse(result)
