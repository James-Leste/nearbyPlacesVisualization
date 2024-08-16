import requests
import json
import numpy
from math import radians, cos, sin, asin, sqrt
import pandas as pd
import csv
import argparse


with open("config.json") as f:
    api_key = json.load(f)["api_key"]

fieldMask = "places.name,places.nationalPhoneNumber,places.types,places.formattedAddress,places.addressComponents,places.rating,places.businessStatus,places.userRatingCount,places.dineIn,places.displayName,places.googleMapsUri"

headers = {
    'X-Goog-Api-Key': api_key,
    'X-Goog-FieldMask': fieldMask
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
rectangle = [[61.5002, 23.7518], [61.4916, 23.7882]]
# rectangle = [[61.5002, 23.7818], [61.4989, 23.7882]]

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
    print(f'total raw results: {total}')
    return total

# combine all the json results
def combineJson(split_factors):

    combinedPlaces = []

    for x in range(0, split_factors[0]):
        for y in range(0, split_factors[1]):
            data = pd.read_json(f'./results/{x}-{y}.json')
            if('places' in data):
                combinedPlaces.extend(data["places"])
            else:
                continue
    combinedJson = {'places': combinedPlaces}
    print(f'summary length: {len(combinedJson["places"])}')
    return combinedJson

def extract_postal_code(address_components):
    for component in address_components:
        if "postal_code" in component["types"]:
            
            return component["longText"]
    return None

def extract_city_name(address_components):
    for component in address_components:
        if "administrative_area_level_2" in component["types"]:
            
            return component["longText"]
    return None


def write_csv (split_factors):
    csv_data = []
    for idx, place in enumerate(combineJson(split_factors)['places']):
        name = place['name']
        display_name = place['displayName']['text']
        postal_code = extract_postal_code(place['addressComponents'])
        
        google_maps_uri = place['googleMapsUri']
        restaurant_type = place['types'] if 'types' in place else ''
        city_name = extract_city_name(place['addressComponents'])
        business_status = place['businessStatus'] if 'business' in place else ''
        nationalPhoneNumber = place['nationalPhoneNumber'] if 'nationalPhoneNumber' in place else ''
        rating = place['rating'] if 'rating' in place else ''
        dineIn = place['dineIn'] if 'dineIn' in place else ''
        
        csv_data.append([idx, name, display_name, restaurant_type, postal_code, city_name, business_status, nationalPhoneNumber, rating, dineIn, google_maps_uri])

    csv_header = ['Index', 'Name', 'DisplayName', 'restaurant_type', 'PostalCode', 'city_name', 'business_status', 'nationalPhoneNumber', 'rating', 'dineIn', 'GoogleMapsUri']
    with open('./results/summary.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(csv_header)
        writer.writerows(csv_data)

def clean_data():
    csvdata = pd.read_csv('./results/summary.csv', dtype={"PostalCode": str})
    clean_data = csvdata.drop_duplicates(subset=["Name"]).reset_index(drop=True)
    clean_data.to_csv("./results/result.csv")
    print(f'actual_quantity: {len(clean_data)}')
    return len(clean_data)


if __name__ == "__main__":
    search(area, "restaurant", split_factors)
    write_csv(split_factors)
    clean_data()






