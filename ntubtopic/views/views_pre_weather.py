from django.http import JsonResponse
from ntubtopic.models import *
import json


def PostPreWeather(request):
    result = {'result': 0}
    db_locations = PreWeather.objects.all()
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
                result['NowStartDate'] = b.today_startdate
                result['NowStartTime'] = b.today_starttime
                result['NowEndDate'] = b.today_enddate
                result['NowEndTime'] = b.today_endtime
                result['NowMaxT'] = b.today_maxt
                result['NowMinT'] = b.today_mint
                result['NowPoP'] = b.today_pop
                result['NowWx'] = b.today_wx

                result['CloseStartDate'] = b.today_startdate_field
                result['CloseStartTime'] = b.today_starttime_field
                result['CloseEndDate'] = b.today_enddate_field
                result['CloseEndTime'] = b.today_endtime_field
                result['CloseMaxT'] = b.today_maxt_field
                result['CloseMinT'] = b.today_mint_field
                result['ClosePoP'] = b.today_pop_field
                result['CloseWx'] = b.today_wx_field

                result['FarStartDate'] = b.tomorrow_startdate
                result['FarStartTime'] = b.tomorrow_starttime
                result['FarEndDate'] = b.tomorrow_enddate
                result['FarEndTime'] = b.tomorrow_endtime
                result['FarMaxT'] = b.tomorrow_maxt
                result['FarMinT'] = b.tomorrow_mint
                result['FarPoP'] = b.tomorrow_pop
                result['FarWx'] = b.tomorrow_wx

    except Exception as e:
        result['error'] = str(e)

    return JsonResponse(result)
