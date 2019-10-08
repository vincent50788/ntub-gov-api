# from django.shortcuts import render
from django.http import JsonResponse
from ntubtopic.models import *
import json


def PostEnvironmentalWarning(request):
    result = {'result': 0}
    db_locations = Alerts.objects.all()
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
                result['city'] = b.city
                result['warning'] = b.hazard
                result['date'] = b.date
                result['time'] = b.time
    except Exception as e:
        result['error'] = str(e)

    return JsonResponse(result)

