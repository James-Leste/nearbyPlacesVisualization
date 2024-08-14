import requests
import json
import numpy
from math import radians, cos, sin, asin, sqrt



with open("config.json") as f:
    api_key = json.load(f)["api_key"]

headers = {
    'X-Goog-Api-Key': api_key,
    'X-Goog-FieldMask': 'places.name,places.googleMapsUri,places.displayName,places.addressComponents'
}

# calculate distance between two locations
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
# calculate the width and length of a rectangle area
def distance_metrix(rectangle):

    lonDistance = distance(rectangle[0][0], rectangle[0][0], rectangle[0][1], rectangle[1][1]) * 1000
    latDistance = distance(rectangle[0][0], rectangle[1][0], rectangle[1][1], rectangle[1][1]) * 1000

    return([latDistance, lonDistance])


# rectangle[0] upper left
# rectangle[1] bottom right
rectangle = [[60.1699, 24.9298], [60.1660, 24.9414]]

metrix = distance_metrix(rectangle)
print(f"metrix: {metrix}")

# metre
radius = 100

split_factors = [int(metrix[0]//radius), int(metrix[1]//radius)]
print(f"split_factors: {split_factors}")

area = {
    'metrix': distance_metrix(rectangle),
    'rectangle': rectangle, 
    'radius': radius
}

def search(area, type, split_factors):
    total = 0
    for rowIndex, lat in enumerate(numpy.linspace(rectangle[1][0], rectangle[0][0], num=split_factors[0])):
        for colomnIndex, lon in enumerate(numpy.linspace(rectangle[1][1], rectangle[0][1], num=split_factors[1])):
            data = {
                "includedTypes": [
                    type
                ],
                "maxResultCount": 20,
                "locationRestriction": {
                    "circle": {
                        "center": {
                            "latitude": lat,
                            "longitude": lon
                        },
                        "radius": area["radius"]
                    }
                },
                "rankPreference": "DISTANCE"
            }
            r = requests.post('https://places.googleapis.com/v1/places:searchNearby', json=data, headers=headers)
            if("places" in r.json()):
                print(f'{rowIndex}-{colomnIndex}: {len(r.json()["places"])} results')
                total += len(r.json()["places"])
            else:
                print(f'{rowIndex}-{colomnIndex}: 0 result')

            with open(f"./results/{rowIndex}-{colomnIndex}.json", "w") as jsonfile:
                jsonfile.write(r.text)
    print(total)
    return total


search(area, "restaurant", split_factors)


# r = requests.post('https://places.googleapis.com/v1/places:searchNearby', json=data, headers=headers)

# print(r.json())
# with open(f"./results/.json", "w") as jsonfile:
#     jsonfile.write(r.text)
