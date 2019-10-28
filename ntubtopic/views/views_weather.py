# from django.shortcuts import render
from django.http import JsonResponse
from ntubtopic.models import *
import json


def dirTran(value):
    try:
        value = float(value)
        if value >= 348.76 or value <= 11.25:
            return "N"
        elif value >= 11.26 and value <= 33.75:
            return "NNE"
        elif value >= 33.76 and value <= 56.25:
            return "NE"
        elif value >= 56.26 and value <= 78.75:
            return "ENE"
        elif value >= 78.76 and value <= 101.25:
            return "E"
        elif value >= 101.26 and value <= 123.75:
            return "ESE"
        elif value >= 123.76 and value <= 146.25:
            return "SE"
        elif value >= 146.26 and value <= 168.75:
            return "SSE"
        elif value >= 168.76 and value <= 191.25:
            return "S"
        elif value >= 191.26 and value <= 213.75:
            return "SSW"
        elif value >= 213.76 and value <= 236.25:
            return "SW"
        elif value >= 236.26 and value <= 258.75:
            return "WSW"
        elif value >= 258.76 and value <= 281.25:
            return "W"
        elif value >= 281.26 and value <= 303.75:
            return "WNW"
        elif value >= 303.76 and value <= 326.25:
            return "NW"
        elif value >= 326.26 and value <= 348.75:
            return "NNW"
        else:
            return "靜風"

    except ValueError:
        return value


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
                result['windDir'] = dirTran(b.wind_dir)
                result['windSpeed'] = b.wind_speed
                result['tempNow'] = b.temp_now.split(".", 1)[0]
                result['humidity'] = b.humd.split(".", 1)[1] + "%"
                result['rainFall'] = b.rainfall
                result['uviH'] = b.h_uvi
                result['uviStatus'] = b.uvi_status
                result['tempMax'] = b.temp_max.split(".", 1)[0]
                result['tempMaxTime'] = b.tmax_time
                result['tempMin'] = b.temp_min.split(".", 1)[0]
                result['tempMinTime'] = b.tmin_time

    except Exception as e:
        result['error'] = str(e)

    return JsonResponse(result)


