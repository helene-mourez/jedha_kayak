# import libraries

import json
import time
import os

import requests
from dotenv import load_dotenv
import pandas as pd

def one_city():
    nominatim_url = "https://nominatim.openstreetmap.org/search"
    cities_info = f"{nominatim_url}/cities_location.json"

    params = {
        "country": "France",
        "city": "Bayeux",
        "format": "geocodejson"
    }

    headers = {"User-Agent": "projet_etude_dataviz (lnmourez@gmail.com)"}

    response = requests.get(nominatim_url, params=params, headers=headers) # call api

    feature = response.json()["features"][0] # declare the first result
    city = feature["properties"]["geocoding"]["name"]
    place_id = feature["properties"]["geocoding"]["place_id"]
    lat = feature["geometry"]["coordinates"][1]
    lon = feature["geometry"]["coordinates"][0]

    return print(f"{response.status_code}, {city}, {place_id},{lon}, {lat}")

def get_city(cities):
    '''
    CALL API NOMINATIM

    Realised with Nominatim 5.3.2 manual : https://nominatim.org/release-docs/latest/
    '''

    nominatim_url = "https://nominatim.openstreetmap.org/search"
    # cities_info = f"{nominatim_url}/cities_location.json"

    # params = {
    #    "country": "France",
    #    "city": "Bayeux",
    #    "format": "geocodejson"
    # }

    headers = {"User-Agent": "projet_etude_dataviz (lnmourez@gmail.com)"}
    # nominatim_response = requests.get(nominatim_url, params=params, headers=headers) # call api

    # print(nominatim_response) # call api status code 

    cities_info = []
    
    response = []
    for city in cities:
        try:
            nominatim_response = requests.get(
                nominatim_url, 
                params={"country": "France",
                "city": city,
                "format": "geocodejson"
                },
                headers=headers)

            if nominatim_response.status_code==200 :
                response.append(200) # compteur status code = 200 sur les appels
            feature = nominatim_response.json()["features"][0]
            cities_info.append({"city" : feature["properties"]["geocoding"]["name"],
            "place_id" : feature["properties"]["geocoding"]["place_id"],
            "lat" : feature["geometry"]["coordinates"][1],
            "lon" : feature["geometry"]["coordinates"][0]
            })
            
        except (IndexError, KeyError, requests.exceptions.RequestException):
            print(f"Execution with errors for {city} : {nominatim_response.status_code}")
        
        time.sleep(2) 
    print(len(response)) # liste de dictionnaires
    # print(cities_info)
    return cities_info


##### script tests ####
if __name__ == "__main__": # ce test s'exécute seulement si le fichier est lancé directement
    print(one_city())
    print(get_city())