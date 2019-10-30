from django.http import JsonResponse
from superCrawler import bike_crawler
import json


def get_all_bikes(request):
    datas = bike_crawler()
    bikes = []
    result = {'result': 0}
    data = json.loads(request.body.decode(encoding="utf-8"))
    user_type = data['GetBike']

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
    datas = bike_crawler()
    results = {'result': 0}
    hypotenuse_list = []
    if datas:

        data = json.loads(request.body.decode(encoding="utf-8"))
        user_type = data['type']
        user_long = data['Longitude']
        user_lat = data['Latitude']



        try:
            if user_type == "1":  # 自己最近腳踏車站

                for a in datas:
                    db_long = a['StationLongitude']
                    db_lat = a['StationLatitude']
                    hypotenuse = (float(db_long) - float(user_long)) ** 2 + (float(db_lat) - float(user_lat)) ** 2
                    hypotenuse_list.append(hypotenuse)

                min_hypotenuse = min(hypotenuse_list)

                for b in datas:

                    if min_hypotenuse == (float(b['StationLongitude']) - float(user_long)) ** 2 + (float(b['StationLatitude']) - float(user_lat)) ** 2:
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

            elif user_type == "2":      # 自己最近有可租借bike站點
                availbiksList = []

                for a in datas:
                    if a['AvailableRentBikes'] > 0 and a['ServieAvailable'] == 1:
                        availbiksList.append(a)

                for b in availbiksList:
                    db_long = b['StationLongitude']
                    db_lat = b['StationLatitude']
                    hypotenuse = (float(db_long) - float(user_long)) ** 2 + (float(db_lat) - float(user_lat)) ** 2
                    hypotenuse_list.append(hypotenuse)
                min_hypotenuse = min(hypotenuse_list)

                for c in availbiksList:

                    if min_hypotenuse == (float(c['StationLongitude']) - float(user_long)) ** 2 + (float(c['StationLatitude']) - float(user_lat)) ** 2:
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

            elif user_type == "3":      # 自己最近有可歸還bike站點
                availbiksList = []

                for a in datas:
                    if a['AvailableReturnBikes'] > 0 and a['ServieAvailable'] == 1:
                        availbiksList.append(a)

                for b in availbiksList:
                    db_long = b['StationLongitude']
                    db_lat = b['StationLatitude']
                    hypotenuse = (float(db_long) - float(user_long)) ** 2 + (float(db_lat) - float(user_lat)) ** 2
                    hypotenuse_list.append(hypotenuse)
                min_hypotenuse = min(hypotenuse_list)

                for c in availbiksList:

                    if min_hypotenuse == (float(c['StationLongitude']) - float(user_long)) ** 2 + (float(c['StationLatitude']) - float(user_lat)) ** 2:
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


