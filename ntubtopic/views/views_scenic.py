from django.http import JsonResponse
from superCrawler import scenicSpot_crawler
import json


def PostScenicSpot(request):
    result = {'result': 0}
    db_locations = scenicSpot_crawler()
    data = json.loads(request.body.decode(encoding="utf-8"))
    hypotenuse_list = []
    user_long = data['Longitude']
    user_lat = data['Latitude']
    type = data['type']
    scenics = []
    for a in db_locations:
        db_long = a['ScenicLongitude']
        db_lat = a['ScenicLatitude']
        hypotenuse = (float(db_long) - float(user_long)) ** 2 + (float(db_lat) - float(user_lat)) ** 2
        hypotenuse_list.append(hypotenuse)

    min_hypotenuse = min(hypotenuse_list)
    sort_hypotenuse = sorted(hypotenuse_list)

    if type == "1":
        try:
            for b in db_locations:
                if min_hypotenuse == (float(b['ScenicLongitude']) - float(user_long)) ** 2 + (float(b['ScenicLatitude']) - float(user_lat)) ** 2:
                    result['result'] = 1
                    result['ScenicName'] = b['ScenicName']
                    result['ScenicAddress'] = b['ScenicAddress']
                    result['ScenicDescription'] = b['ScenicDescription']
                    result['ScenicLongitude'] = b['ScenicLongitude']
                    result['ScenicLatitude'] = b['ScenicLatitude']
                    result['ScenicPhone'] = b['ScenicPhone']
                    result['ScenicOpentime'] = b['ScenicOpentime']

        except Exception as e:
            result['error'] = str(e)

        return JsonResponse(result)

    elif type == '2':
        try:
            for a in range(len(sort_hypotenuse)):
                for b in db_locations:
                    if sort_hypotenuse[a] == (float(b['ScenicLongitude']) - float(user_long)) ** 2 + (float(b['ScenicLatitude']) - float(user_lat)) ** 2:
                        scenic = {}
                        scenic['ScenicName'] = b['ScenicName']
                        scenic['ScenicAddress'] = b['ScenicAddress']
                        scenic['ScenicLongitude'] = b['ScenicLongitude']
                        scenic['ScenicLatitude'] = b['ScenicLatitude']
                        scenic['ScenicPhone'] = b['ScenicPhone']
                        scenic['ScenicOpentime'] = b['ScenicOpentime']
                        scenics.append(scenic)

                if len(scenics) == 0:
                    result['result'] = 1
                    result['type'] = '由近到遠'
                    scenics.append({'error': '連線異常，請稍後再試'})
                    result['scenics'] = scenics
                else:
                    result['result'] = 1
                    result['type'] = '由近到遠'
                    result['scenics'] = scenics

        except Exception as e:
            result['error'] = str(e)

        return JsonResponse(result)