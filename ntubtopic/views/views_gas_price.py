from django.shortcuts import render
from django.http import JsonResponse
from ntubtopic.models import *
import json

# Create your views here.

'''
def GetOilPrice(request):
    result = {'result': 0}
    dbprices = Oils.objects.all()

    if len(dbprices) > 0:
        for a in dbprices:
            result['result'] = 1
            result['92'] = a.unleaded
            result['95'] = a.super
            result['98'] = a.supreme
            result['alcoholGas'] = a.alcohol_gas
            result['diesel'] = a.diesel  # 超柴
            result['liquefiedGas'] = a.liquefied_gas

    return JsonResponse(result)

'''


def PostOilPrice(request):
    result = {'result': 0}
    db_oil_price = Oils.objects.all()
    data = json.loads(request.body.decode(encoding="utf-8"))
    user_data = data['GetPrice']
    if user_data == 1:
        for a in db_oil_price:
            result['unleaded'] = a.unleaded
            result['super_'] = a.super
            result['supreme'] = a.supreme
            result['alcoholGas'] = a.alcohol_gas
            result['diesel'] = a.diesel  # 超柴
            result['liquefiedGas'] = a.liquefied_gas

        result['result'] = 1

    return JsonResponse(result)
