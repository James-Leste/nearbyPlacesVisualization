import requests
import json
import numpy
from math import radians, cos, sin, asin, sqrt

with open("config.json") as f:
    api_key = json.load(f)["api_key"]

def distance (lat1, lat2, lon1, lon2): 
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)

    dlon = lon2 - lon1 
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
 
    c = 2 * asin(sqrt(a)) 
    
    # Radius of earth in kilometers. Use 3956 for miles
    r = 6371

    return c * r

# rectangle[0] upper left
# rectangle[1] bottom right
def distance_metrix(rectangle):

    width = distance(rectangle[0][0], rectangle[0][0], rectangle[0][1], rectangle[1][1]) * 1000
    length = distance(rectangle[0][0], rectangle[1][0], rectangle[1][1], rectangle[1][1]) * 1000

    return([width, length])

split = 6

rectangle = [[60.1699, 24.9298], [60.1660, 24.9414]]

radius = min(distance_metrix(rectangle))/split

area = {
    'metrix': distance_metrix(rectangle),
    'rectangle': rectangle, 
    'radius': radius
}

headers = {
    'X-Goog-Api-Key': api_key,
    'X-Goog-FieldMask': 'places.displayName'
}

def search(rectangle, type, spilt, radius):
    for rowIndex, lat in enumerate(numpy.linspace(rectangle[1][0], rectangle[0][0], num=split)):
        for colomnIndex, lon in enumerate(numpy.linspace(rectangle[1][1], rectangle[0][1], num=split)):
            data = {
                "includedTypes": [
                    "restaurant"
                ],
                "maxResultCount": 20,
                "locationRestriction": {
                    "circle": {
                        "center": {
                            "latitude": lat,
                            "longitude": lon
                        },
                        "radius": radius
                    }
                },
                "rankPreference": "DISTANCE"
            }
            r = requests.post('https://places.googleapis.com/v1/places:searchNearby', json=data, headers=headers)
            if("places" in r.json()):
                print(f'{rowIndex}-{colomnIndex}: {len(r.json()["places"])}')
            else:
                print(f'{rowIndex}-{colomnIndex}: 0')

            with open(f"./results/{rowIndex}-{colomnIndex}.json", "w") as jsonfile:
                jsonfile.write(r.text)


search(rectangle, "restaurant", split, radius)




# r = requests.post('https://places.googleapis.com/v1/places:searchNearby', json=data, headers=headers)

# print(r.json())
# with open(f"./results/.json", "w") as jsonfile:
#     jsonfile.write(r.text)
