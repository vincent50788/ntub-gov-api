from django.http import JsonResponse
from superCrawler import bike_crawler
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


def get_all_bikes(request):
    bikes = []
    result = {'result': 0}
    data = json.loads(request.body.decode(encoding="utf-8"))
    user_type = data['GetBike']
    user_city = data['City']

    if user_city == 'Taipei':
        datas = bike_crawler('Taipei')
    elif user_city == 'NewTaipei':
        datas = bike_crawler('NewTaipei')
    elif user_city == 'Hsinchu':
        datas = bike_crawler('Hsinchu')
    elif user_city == 'MiaoliCounty':
        datas = bike_crawler('MiaoliCounty')
    elif user_city == 'ChanghuaCounty':
        datas = bike_crawler('ChanghuaCounty')
    elif user_city == 'PingtungCounty':
        datas = bike_crawler('PingtungCounty')
    elif user_city == 'Taoyuan':
        datas = bike_crawler('Taoyuan')
    elif user_city == 'Kaohsiungu':
        datas = bike_crawler('Kaohsiung')
    elif user_city == 'Tainan':
        datas = bike_crawler('Tainan')
    elif user_city == 'Taichung':
        datas = bike_crawler('Taichung')

    try:
        if user_type == "1":
            for a in datas:
                bike = {}

                bike['StationUID'] = a['StationUID']
                bike['StationName_zh'] = a['StationName_zh']
                bike['Longitude'] = a['StationLongitude']
                bike['Latitude'] = a['StationLatitude']
                bike['stationAddress_zh'] = a['stationAddress_zh']
                bike['BikesCapacity'] = str(a['BikesCapacity'])
                bike['ServieAvailable'] = str(a['ServieAvailable'])
                bike['AvailableRentBikes'] = str(a['AvailableRentBikes'])
                bike['AvailableReturnBikes'] = str(a['AvailableReturnBikes'])
                bike['UpdateTime'] = a['UpdateTime']
                bikes.append(bike)

            if len(bikes) == 0:
                result['result'] = 1
                result['type'] = '全部站點'
                bikes.append({'error': '連線異常，請稍後再試'})
                result['bikes'] = bikes
            else:
                result['result'] = 1
                result['type'] = '全部站點'
                result['bikes'] = bikes

    except Exception as e:
        result['error'] = str(e)

    return JsonResponse(result)


def get_close_bike(request):
    data = json.loads(request.body.decode(encoding="utf-8"))
    user_city = data['City']
    user_type = data['type']
    user_long = data['Longitude']
    user_lat = data['Latitude']
    results = {'result': 0}
    havList = []

    # 判斷要那個City
    if user_city == 'Taipei':
        datas = bike_crawler('Taipei')
    elif user_city == 'NewTaipei':
        datas = bike_crawler('NewTaipei')
    elif user_city == 'Hsinchu':
        datas = bike_crawler('Hsinchu')
    elif user_city == 'MiaoliCounty':
        datas = bike_crawler('MiaoliCounty')
    elif user_city == 'ChanghuaCounty':
        datas = bike_crawler('ChanghuaCounty')
    elif user_city == 'PingtungCounty':
        datas = bike_crawler('PingtungCounty')
    elif user_city == 'Taoyuan':
        datas = bike_crawler('Taoyuan')
    elif user_city == 'Kaohsiung':
        datas = bike_crawler('Kaohsiung')
    elif user_city == 'Tainan':
        datas = bike_crawler('Tainan')
    elif user_city == 'Taichung':
        datas = bike_crawler('Taichung')

    if datas:

        for a in datas:
            haver = haversine(user_long, user_lat, float(a['StationLongitude']), float(a['StationLatitude']))
            havList.append(haver)
        havMin = min(havList)

        try:
            if user_type == "1":  # 自己最近腳踏車站

                for b in datas:

                    if havMin == haversine(user_long, user_lat, float(b['StationLongitude']), float(b['StationLatitude'])):
                        results['result'] = 1
                        results['type'] = '自己最近站點'
                        results['StationUID'] = b['StationUID']
                        results['StationName_zh'] = b['StationName_zh']
                        results['Longitude'] = b['StationLongitude']
                        results['Latitude'] = b['StationLatitude']
                        results['stationAddress_zh'] = b['stationAddress_zh']
                        results['BikesCapacity'] = str(b['BikesCapacity'])
                        results['ServieAvailable'] = str(b['ServieAvailable'])
                        results['AvailableRentBikes'] = str(b['AvailableRentBikes'])
                        results['AvailableReturnBikes'] = str(b['AvailableReturnBikes'])
                        results['UpdateTime'] = b['UpdateTime']
                        results['haversine'] = str(havMin).split(".")[0]

            elif user_type == "2":      # 自己最近有可租借bike站點
                availbiksList = []

                for a in datas:
                    if a['AvailableRentBikes'] > 0 and a['ServieAvailable'] == 1:
                        availbiksList.append(a)

                for c in availbiksList:

                    if havMin == haversine(user_long, user_lat, float(c['StationLongitude']), float(c['StationLatitude'])):
                        results['result'] = 1
                        results['type'] = '自己最近有可租借bike站點'
                        results['StationUID'] = c['StationUID']
                        results['StationName_zh'] = c['StationName_zh']
                        results['Longitude'] = c['StationLongitude']
                        results['Latitude'] = c['StationLatitude']
                        results['stationAddress_zh'] = c['stationAddress_zh']
                        results['BikesCapacity'] = str(c['BikesCapacity'])
                        results['ServieAvailable'] = str(c['ServieAvailable'])
                        results['AvailableRentBikes'] = str(c['AvailableRentBikes'])
                        results['AvailableReturnBikes'] = str(c['AvailableReturnBikes'])
                        results['UpdateTime'] = c['UpdateTime']
                        results['haversine'] = str(havMin).split(".")[0]

            elif user_type == "3":      # 自己最近有可歸還bike站點
                availbiksList = []

                for a in datas:
                    if a['AvailableReturnBikes'] > 0 and a['ServieAvailable'] == 1:
                        availbiksList.append(a)

                for c in availbiksList:

                    if havMin == haversine(user_long, user_lat, float(c['StationLongitude']), float(c['StationLatitude'])):
                        results['result'] = 1
                        results['type'] = '自己最近有可歸還bike站點'
                        results['StationUID'] = c['StationUID']
                        results['StationName_zh'] = c['StationName_zh']
                        results['Longitude'] = c['StationLongitude']
                        results['Latitude'] = c['StationLatitude']
                        results['stationAddress_zh'] = c['stationAddress_zh']
                        results['BikesCapacity'] = str(c['BikesCapacity'])
                        results['ServieAvailable'] = str(c['ServieAvailable'])
                        results['AvailableRentBikes'] = str(c['AvailableRentBikes'])
                        results['AvailableReturnBikes'] = str(c['AvailableReturnBikes'])
                        results['UpdateTime'] = c['UpdateTime']
                        results['haversine'] = str(havMin).split(".")[0]

            else:
                results['result'] = 1
                results['type'] = 'KeyError'

        except Exception as e:
            results['error'] = str(e)

        return JsonResponse(results)
    else:
        results['result'] = 1
        results['error'] = '主機連線異常，請稍後再試'
        return JsonResponse(results)


