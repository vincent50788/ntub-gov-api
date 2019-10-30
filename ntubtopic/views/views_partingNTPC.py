from django.http import JsonResponse
from superCrawler import parting_ntpc
from math import radians, cos, sin, asin, sqrt
import json


def haversine(lon1, lat1, lon2, lat2):  # 经度1，纬度1，经度2，纬度2 （十进制度数）
    # 将十进制度数转化为弧度
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine公式
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # 地球平均半径，单位为公里
    return c * r * 1000


def PostNTPCPart(request):
    result = {'result': 0}
    parks = []


    havList = []
    parkSpaces = []
    datas = parting_ntpc()

    data = json.loads(request.body.decode(encoding="utf-8"))
    user_long = data['Longitude']
    user_lat = data['Latitude']
    contain = data['contain']  # 0(All)/1(Self)
    type_ = data['type']  # 有無包含 special parking

    if contain == "0" and type_ == '0':  # 所有車位
        try:
            for b in datas:
                park = {}
                haver = haversine(user_long, user_lat, float(b['Longitude']), float(b['Latitude']))

                park['NAME'] = b['NAME']
                park['DAY'] = b['DAY']
                park['HOUR'] = b['HOUR']
                park['PAY'] = b['PAY']
                park['PAYCASH'] = b['CASH']
                park['MEMO'] = b['MEMO']
                park['CellStatus'] = b['Status']
                park['IsNowCash'] = b['IsNowCash']
                park['ParkStatus'] = b['ParkingStatus']
                park['ParkStatusZh'] = b['ParkStatusZh']
                park['Haversine'] = str(haver)
                park['Longitude'] = b['Longitude']
                park['Latitude'] = b['Latitude']
                parks.append(park)

            if len(parks) == 0:
                result['result'] = 1
                result['type'] = '所有車位'
                parks.append({'NAME': '尚無資料'})
                result['parks'] = parks
            else:
                result['result'] = 1
                result['type'] = '所有車位'
                result['parks'] = parks

        except Exception as e:
            result['error'] = str(e)
        return JsonResponse(result, safe=False)

    elif contain == "0" and type_ == "1":  # 所有空車位(不包含 非收費時段 時段性禁停)
        try:
            for b in datas:
                if b['ParkingStatus'] == '2':
                    park = {}
                    haver = haversine(user_long, user_lat, float(b['Longitude']), float(b['Latitude']))
                    park['NAME'] = b['NAME']
                    park['DAY'] = b['DAY']
                    park['HOUR'] = b['HOUR']
                    park['PAY'] = b['PAY']
                    park['PAYCASH'] = b['CASH']
                    park['MEMO'] = b['MEMO']
                    park['CellStatus'] = b['Status']
                    park['IsNowCash'] = b['IsNowCash']
                    park['ParkStatus'] = b['ParkingStatus']
                    park['ParkStatusZh'] = b['ParkStatusZh']
                    park['Haversine'] = str(haver)
                    park['Longitude'] = b['Longitude']
                    park['Latitude'] = b['Latitude']
                    parks.append(park)

            if len(parks) == 0:
                result['result'] = 1
                result['type'] = '所有空車位(不包含 非收費時段 時段性禁停)'
                parks.append({'NAME': '目前無車位'})
                result['parks'] = parks
            else:
                result['result'] = 1
                result['type'] = '所有空車位(不包含 非收費時段 時段性禁停)'
                result['parks'] = parks

        except Exception as e:
            result['error'] = str(e)

        return JsonResponse(result, safe=False)

    elif contain == "0" and type_ == '2':  # 所有空車位(包含 非收費時段 時段性禁停)
        try:
            for b in datas:
                if b['ParkingStatus'] != '1':
                    park = {}
                    haver = haversine(user_long, user_lat, float(b['Longitude']), float(b['Latitude']))

                    park['NAME'] = b['NAME']
                    park['DAY'] = b['DAY']
                    park['HOUR'] = b['HOUR']
                    park['PAY'] = b['PAY']
                    park['PAYCASH'] = b['CASH']
                    park['MEMO'] = b['MEMO']
                    park['CellStatus'] = b['Status']
                    park['IsNowCash'] = b['IsNowCash']
                    park['ParkStatus'] = b['ParkingStatus']
                    park['ParkStatusZh'] = b['ParkStatusZh']
                    park['Haversine'] = str(haver)
                    park['Longitude'] = b['Longitude']
                    park['Latitude'] = b['Latitude']
                    parks.append(park)

            if len(parks) == 0:
                result['result'] = 1
                result['type'] = '所有空車位(包含 非收費時段 時段性禁停)'
                parks.append({'NAME': '目前無車位'})
                result['parks'] = parks
            else:
                result['result'] = 1
                result['type'] = '所有空車位(包含 非收費時段 時段性禁停)'
                result['parks'] = parks

        except Exception as e:
            result['error'] = str(e)
        return JsonResponse(result, safe=False)

    # -------------------------------------------------------------

    elif contain == "1" and type_ == "0":  # 自己最近的一個車位

        for a in datas:
            haver = haversine(user_long, user_lat, float(a['Longitude']), float(a['Latitude']))
            havList.append(haver)
        havMin = min(havList)

        try:
            for b in datas:
                haver = haversine(user_long, user_lat, float(b['Longitude']), float(b['Latitude']))
                if havMin == haver:
                    park = {}
                    park['NAME'] = b['NAME']
                    park['DAY'] = b['DAY']
                    park['HOUR'] = b['HOUR']
                    park['PAY'] = b['PAY']
                    park['PAYCASH'] = b['CASH']
                    park['MEMO'] = b['MEMO']
                    park['CellStatus'] = b['Status']
                    park['IsNowCash'] = b['IsNowCash']
                    park['ParkStatus'] = b['ParkingStatus']
                    park['ParkStatusZh'] = b['ParkStatusZh']
                    park['Haversine'] = str(haver)
                    park['Longitude'] = b['Longitude']
                    park['Latitude'] = b['Latitude']
                    parks.append(park)

            if len(parks) == 0:
                result['result'] = 1
                result['type'] = '自己最近的一個車位'
                parks.append({'NAME': '目前無車位'})
                result['parks'] = parks
            else:
                result['result'] = 1
                result['type'] = '自己最近的一個車位'
                result['parks'] = parks

        except Exception as e:
            result['error'] = str(e)

        return JsonResponse(result, safe=False)

    elif contain == "1" and type_ == "1":  # 自己最近的一個空車位(不包含 非收費時段 時段性禁停)

        for a in datas:
            if a['ParkingStatus'] == '2':
                parkSpaces.append(a)

        for b in parkSpaces:
            haver = haversine(user_long, user_lat, float(b['Longitude']), float(b['Latitude']))
            havList.append(haver)

        if havList:
            havMin = min(havList)

            try:
                for c in parkSpaces:
                    haver = haversine(user_long, user_lat, float(c['Longitude']), float(c['Latitude']))
                    if havMin == haver:
                        park = {}
                        park['NAME'] = c['NAME']
                        park['DAY'] = c['DAY']
                        park['HOUR'] = c['HOUR']
                        park['PAY'] = c['PAY']
                        park['PAYCASH'] = c['CASH']
                        park['MEMO'] = c['MEMO']
                        park['CellStatus'] = c['Status']
                        park['IsNowCash'] = c['IsNowCash']
                        park['ParkStatus'] = c['ParkingStatus']
                        park['ParkStatusZh'] = c['ParkStatusZh']
                        park['Haversine'] = str(haver)
                        park['Longitude'] = c['Longitude']
                        park['Latitude'] = c['Latitude']
                        parks.append(park)

                if len(parks) == 0:
                    result['result'] = 1
                    result['type'] = '自己最近的一個空車位(不包含 非收費時段 時段性禁停)'
                    parks.append({'NAME': '目前無車位'})
                    result['parks'] = parks
                else:
                    result['result'] = 1
                    result['type'] = "自己最近的一個空車位(不包含 非收費時段 時段性禁停)"
                    result['parks'] = parks

            except Exception as e:
                result['error'] = str(e)
            return JsonResponse(result)

        else:
            result['result'] = 1
            result['type'] = '自己最近的一個空車位(不包含 非收費時段 時段性禁停)'
            parks.append({'NAME': '尚無資料'})
            result['parks'] = parks

            return JsonResponse(result)

    elif contain == "1" and type_ == "2":  # 離自己最近的一個空車位(包含 非收費時段 時段性禁停)

        for a in datas:
            if a['ParkingStatus'] != '1':
                parkSpaces.append(a)

        for b in parkSpaces:
            haver = haversine(user_long, user_lat, float(b['Longitude']), float(b['Latitude']))
            havList.append(haver)

        if havList:
            havMin = min(havList)

            try:
                for c in parkSpaces:
                    haver = haversine(user_long, user_lat, float(c['Longitude']), float(c['Latitude']))

                    if havMin == haver:
                        park = {}
                        park['NAME'] = c['NAME']
                        park['DAY'] = c['DAY']
                        park['HOUR'] = c['HOUR']
                        park['PAY'] = c['PAY']
                        park['PAYCASH'] = c['CASH']
                        park['MEMO'] = c['MEMO']
                        park['CellStatus'] = c['Status']
                        park['IsNowCash'] = c['IsNowCash']
                        park['ParkStatus'] = c['ParkingStatus']
                        park['ParkStatusZh'] = c['ParkStatusZh']
                        park['Haversine'] = str(haver)
                        park['Longitude'] = c['Longitude']
                        park['Latitude'] = c['Latitude']
                        parks.append(park)
                if len(parks) == 0:
                    result['result'] = 1
                    result['type'] = '離自己最近的一個空車位(包含 非收費時段 時段性禁停)'
                    parks.append({'NAME': '尚無資料'})
                    result['parks'] = parks
                else:
                    result['result'] = 1
                    result['type'] = "離自己最近的一個空車位(包含 非收費時段 時段性禁停)"
                    result['parks'] = parks

            except Exception as e:
                result['error'] = str(e)

            return JsonResponse(result)
        else:
            result['result'] = 1
            result['type'] = '離自己最近的一個空車位(包含 非收費時段 時段性禁停)'
            parks.append({'NAME': '尚無資料'})
            result['parks'] = parks
            return JsonResponse(result)

    # -------------------------------------------------------------

    elif contain == "1" and type_ == "3":  # 離自己500m所有車位

        try:
            for b in datas:
                haver = haversine(user_long, user_lat, float(b['Longitude']), float(b['Latitude']))
                if haver <= 500:
                    park = {}
                    park['NAME'] = b['NAME']
                    park['DAY'] = b['DAY']
                    park['HOUR'] = b['HOUR']
                    park['PAY'] = b['PAY']
                    park['PAYCASH'] = b['CASH']
                    park['MEMO'] = b['MEMO']
                    park['CellStatus'] = b['Status']
                    park['IsNowCash'] = b['IsNowCash']
                    park['ParkStatus'] = b['ParkingStatus']
                    park['ParkStatusZh'] = b['ParkStatusZh']
                    park['Haversine'] = str(haver)
                    park['Longitude'] = b['Longitude']
                    park['Latitude'] = b['Latitude']
                    parks.append(park)

            if len(parks) == 0:
                result['result'] = 1
                result['type'] = '離自己500m所有車位'
                parks.append({'NAME': '目前無車位'})
                result['parks'] = parks
            else:
                result['result'] = 1
                result['type'] = "離自己500m所有車位"
                result['parks'] = parks
        except Exception as e:
            result['error'] = str(e)

        return JsonResponse(result, safe=False)

    elif contain == "1" and type_ == "4":  # 離自己500m的所有空車位(不包含 非收費時段 時段性禁停)

        for a in datas:
            if a['ParkingStatus'] == '2':  # 不包含 非收費時段 時段性禁停
                parkSpaces.append(a)
        try:
            for c in parkSpaces:
                haver = haversine(user_long, user_lat, float(c['Longitude']), float(c['Latitude']))
                if haver <= 500:
                    park = {}
                    park['NAME'] = c['NAME']
                    park['DAY'] = c['DAY']
                    park['HOUR'] = c['HOUR']
                    park['PAY'] = c['PAY']
                    park['PAYCASH'] = c['CASH']
                    park['MEMO'] = c['MEMO']
                    park['CellStatus'] = c['Status']
                    park['IsNowCash'] = c['IsNowCash']
                    park['ParkStatus'] = c['ParkingStatus']
                    park['ParkStatusZh'] = c['ParkStatusZh']
                    park['Haversine'] = str(haver)
                    park['Longitude'] = c['Longitude']
                    park['Latitude'] = c['Latitude']
                    parks.append(park)

            if len(parks) == 0:
                result['result'] = 1
                result['type'] = '離自己500m的所有空車位(不包含 非收費時段 時段性禁停)'
                parks.append({'NAME': '目前無車位'})
                result['parks'] = parks
            else:
                result['result'] = 1
                result['type'] = "離自己500m的所有空車位(不包含 非收費時段 時段性禁停)"
                result['parks'] = parks

        except Exception as e:
            result['error'] = str(e)

        return JsonResponse(result)

    elif contain == "1" and type_ == "5":  # 離自己500m的所有空車位(包含 非收費時段 時段性禁停)

        for a in datas:
            if a['ParkingStatus'] != '1':  # 包含 非收費時段 時段性禁停
                parkSpaces.append(a)
        try:
            for c in parkSpaces:
                haver = haversine(user_long, user_lat, float(c['Longitude']), float(c['Latitude']))
                if haver <= 500:
                    park = {}
                    park['NAME'] = c['NAME']
                    park['DAY'] = c['DAY']
                    park['HOUR'] = c['HOUR']
                    park['PAY'] = c['PAY']
                    park['PAYCASH'] = c['CASH']
                    park['MEMO'] = c['MEMO']
                    park['CellStatus'] = c['Status']
                    park['IsNowCash'] = c['IsNowCash']
                    park['ParkStatus'] = c['ParkingStatus']
                    park['ParkStatusZh'] = c['ParkStatusZh']
                    park['Haversine'] = str(haver)
                    park['Longitude'] = c['Longitude']
                    park['Latitude'] = c['Latitude']
                    parks.append(park)

            if len(parks) == 0:
                result['result'] = 1
                result['type'] = '離自己500m的所有空車位(包含 非收費時段 時段性禁停)'
                parks.append({'NAME': '目前無車位'})
                result['parks'] = parks
            else:
                result['result'] = 1
                result['type'] = "離自己500m的所有空車位(包含 非收費時段 時段性禁停)"
                result['parks'] = parks
        except Exception as e:
            result['error'] = str(e)

        return JsonResponse(result)

    # -------------------------------------------------------------

    elif contain == "1" and type_ == "6":  # 離自己1000m所有車位

        try:
            for b in datas:
                haver = haversine(user_long, user_lat, float(b['Longitude']), float(b['Latitude']))
                if haver <= 1000:
                    park = {}
                    park['NAME'] = b['NAME']
                    park['DAY'] = b['DAY']
                    park['HOUR'] = b['HOUR']
                    park['PAY'] = b['PAY']
                    park['PAYCASH'] = b['CASH']
                    park['MEMO'] = b['MEMO']
                    park['CellStatus'] = b['Status']
                    park['IsNowCash'] = b['IsNowCash']
                    park['ParkStatus'] = b['ParkingStatus']
                    park['ParkStatusZh'] = b['ParkStatusZh']
                    park['Haversine'] = str(haver)
                    park['Longitude'] = b['Longitude']
                    park['Latitude'] = b['Latitude']
                    parks.append(park)

            if len(parks) == 0:
                result['result'] = 1
                result['type'] = '離自己1000m所有車位'
                parks.append({'NAME': '目前無車位'})
                result['parks'] = parks
            else:
                result['result'] = 1
                result['type'] = "離自己1000m所有車位"
                result['parks'] = parks
        except Exception as e:
            result['error'] = str(e)

        return JsonResponse(result, safe=False)

    elif contain == "1" and type_ == "7":  # 離自己1000m的所有空車位(不包含 非收費時段 時段性禁停)

        for a in datas:
            if a['ParkingStatus'] == '2':  # 不包含 非收費時段 時段性禁停
                parkSpaces.append(a)
        try:
            for c in parkSpaces:
                haver = haversine(user_long, user_lat, float(c['Longitude']), float(c['Latitude']))
                if haver <= 1000:
                    park = {}
                    park['NAME'] = c['NAME']
                    park['DAY'] = c['DAY']
                    park['HOUR'] = c['HOUR']
                    park['PAY'] = c['PAY']
                    park['PAYCASH'] = c['CASH']
                    park['MEMO'] = c['MEMO']
                    park['CellStatus'] = c['Status']
                    park['IsNowCash'] = c['IsNowCash']
                    park['ParkStatus'] = c['ParkingStatus']
                    park['ParkStatusZh'] = c['ParkStatusZh']
                    park['Haversine'] = str(haver)
                    park['Longitude'] = c['Longitude']
                    park['Latitude'] = c['Latitude']
                    parks.append(park)

            if len(parks) == 0:
                result['result'] = 1
                result['type'] = '離自己1000m的所有空車位(不包含 非收費時段 時段性禁停)'
                parks.append({'NAME': '目前無車位'})
                result['parks'] = parks
            else:
                result['result'] = 1
                result['type'] = "離自己1000m的所有空車位(不包含 非收費時段 時段性禁停)"
                result['parks'] = parks

        except Exception as e:
            result['error'] = str(e)

        return JsonResponse(result)

    elif contain == "1" and type_ == "8":  # 離自己1000m的所有空車位(包含 非收費時段 時段性禁停)

        for a in datas:
            if a['ParkingStatus'] != '1':  # 包含 非收費時段 時段性禁停
                parkSpaces.append(a)
        try:
            for c in parkSpaces:
                haver = haversine(user_long, user_lat, float(c['Longitude']), float(c['Latitude']))
                if haver <= 1000:
                    park = {}
                    park['NAME'] = c['NAME']
                    park['DAY'] = c['DAY']
                    park['HOUR'] = c['HOUR']
                    park['PAY'] = c['PAY']
                    park['PAYCASH'] = c['CASH']
                    park['MEMO'] = c['MEMO']
                    park['CellStatus'] = c['Status']
                    park['IsNowCash'] = c['IsNowCash']
                    park['ParkStatus'] = c['ParkingStatus']
                    park['ParkStatusZh'] = c['ParkStatusZh']
                    park['Haversine'] = str(haver)
                    park['Longitude'] = c['Longitude']
                    park['Latitude'] = c['Latitude']
                    parks.append(park)

            if len(parks) == 0:
                result['result'] = 1
                result['type'] = '離自己1000m的所有空車位(包含 非收費時段 時段性禁停)'
                parks.append({'NAME': '目前無車位'})
                result['parks'] = parks
            else:
                result['result'] = 1
                result['type'] = "離自己1000m的所有空車位(包含 非收費時段 時段性禁停)"
                result['parks'] = parks
        except Exception as e:
            result['error'] = str(e)

        return JsonResponse(result)

    # -------------------------------------------------------------

    elif contain == "1" and type_ == "9":  # 離自己1500m所有車位

        try:
            for b in datas:
                haver = haversine(user_long, user_lat, float(b['Longitude']), float(b['Latitude']))
                if haver <= 1500:
                    park = {}
                    park['NAME'] = b['NAME']
                    park['DAY'] = b['DAY']
                    park['HOUR'] = b['HOUR']
                    park['PAY'] = b['PAY']
                    park['PAYCASH'] = b['CASH']
                    park['MEMO'] = b['MEMO']
                    park['CellStatus'] = b['Status']
                    park['IsNowCash'] = b['IsNowCash']
                    park['ParkStatus'] = b['ParkingStatus']
                    park['ParkStatusZh'] = b['ParkStatusZh']
                    park['Haversine'] = str(haver)
                    park['Longitude'] = b['Longitude']
                    park['Latitude'] = b['Latitude']
                    parks.append(park)

            if len(parks) == 0:
                result['result'] = 1
                result['type'] = '離自己1500m所有車位'
                parks.append({'NAME': '目前無車位'})
                result['parks'] = parks
            else:
                result['result'] = 1
                result['type'] = "離自己1500m所有車位"
                result['parks'] = parks
        except Exception as e:
            result['error'] = str(e)

        return JsonResponse(result, safe=False)

    elif contain == "1" and type_ == "10":  # 離自己500m的所有空車位(不包含 非收費時段 時段性禁停)

        for a in datas:
            if a['ParkingStatus'] == '2':  # 不包含 非收費時段 時段性禁停
                parkSpaces.append(a)
        try:
            for c in parkSpaces:
                haver = haversine(user_long, user_lat, float(c['Longitude']), float(c['Latitude']))
                if haver <= 1500:
                    park = {}
                    park['NAME'] = c['NAME']
                    park['DAY'] = c['DAY']
                    park['HOUR'] = c['HOUR']
                    park['PAY'] = c['PAY']
                    park['PAYCASH'] = c['CASH']
                    park['MEMO'] = c['MEMO']
                    park['CellStatus'] = c['Status']
                    park['IsNowCash'] = c['IsNowCash']
                    park['ParkStatus'] = c['ParkingStatus']
                    park['ParkStatusZh'] = c['ParkStatusZh']
                    park['Haversine'] = str(haver)
                    park['Longitude'] = c['Longitude']
                    park['Latitude'] = c['Latitude']
                    parks.append(park)

            if len(parks) == 0:
                result['result'] = 1
                result['type'] = '離自己1500m的所有空車位(不包含 非收費時段 時段性禁停)'
                parks.append({'NAME': '目前無車位'})
                result['parks'] = parks
            else:
                result['result'] = 1
                result['type'] = "離自己1500m的所有空車位(不包含 非收費時段 時段性禁停)"
                result['parks'] = parks

        except Exception as e:
            result['error'] = str(e)

        return JsonResponse(result)

    elif contain == "1" and type_ == "11":  # 離自己500m的所有空車位(包含 非收費時段 時段性禁停)

        for a in datas:
            if a['ParkingStatus'] != '1':  # 包含 非收費時段 時段性禁停
                parkSpaces.append(a)
        try:
            for c in parkSpaces:
                haver = haversine(user_long, user_lat, float(c['Longitude']), float(c['Latitude']))
                if haver <= 1500:
                    park = {}
                    park['NAME'] = c['NAME']
                    park['DAY'] = c['DAY']
                    park['HOUR'] = c['HOUR']
                    park['PAY'] = c['PAY']
                    park['PAYCASH'] = c['CASH']
                    park['MEMO'] = c['MEMO']
                    park['CellStatus'] = c['Status']
                    park['IsNowCash'] = c['IsNowCash']
                    park['ParkStatus'] = c['ParkingStatus']
                    park['ParkStatusZh'] = c['ParkStatusZh']
                    park['Haversine'] = str(haver)
                    park['Longitude'] = c['Longitude']
                    park['Latitude'] = c['Latitude']
                    parks.append(park)

            if len(parks) == 0:
                result['result'] = 1
                result['type'] = '離自己1500m的所有空車位(包含 非收費時段 時段性禁停)'
                parks.append({'NAME': '目前無車位'})
                result['parks'] = parks
            else:
                result['result'] = 1
                result['type'] = "離自己1500m的所有空車位(包含 非收費時段 時段性禁停)"
                result['parks'] = parks
        except Exception as e:
            result['error'] = str(e)

        return JsonResponse(result)

    else:
        result['result'] = 1
        result['type'] = 'KeyError'
        return JsonResponse(result)
