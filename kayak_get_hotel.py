# Libraries import

import requests
import json
import time
from dotenv import load_dotenv
import os
import pandas as pd

# Configuration

# pd.set_option('display.max_columns', None) # display each column's dataframe

def get_city():
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
    cities = ["Aigues Mortes",
    "Aix en Provence",
    "Amiens",
    "Annecy",
    "Avignon",
    "Barjols",
    "Bayeux",
    "Bayonne",
    "Besancon",
    "Biarritz",
    "Bormes les Mimosas",
    "Bédeilhac-et-Aynat",
    "Camon",
    "Carcassonne",
    "Carla-Bayle",
    "Cassis",
    "Castellane",
    "Collioure",
    "Colmar",
    "Cotignac",
    "Dijon",
    "Eguisheim",
    "Foix",
    "Grenoble",
    "La Rochelle",
    "Le Havre",
    "Le Mas-d’Azil",
    "Lille",
    "Lyon",
    "Marseille",
    "Mirepoix",
    "Mont Saint Michel",
    "Montauban",
    "Montségur",
    "Moustiers-Sainte-Marie",
    "Niaux",
    "Nimes",
    "Orschwiller",
    "Paris",
    "Rouen",
    "Saint-Lizier",
    "Saint-Martin-d’Oydes",
    "Sainte-Croix-du-Verdon",
    "Saintes Maries de la mer",
    "Sillans-la-Cascade",
    "St Malo",
    "Strasbourg",
    "Tarascon-sur-Ariège",
    "Toulouse",
    "Uzes",
    "Valensole"
    ]
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
    return cities_info, print(len(response)) # liste de dictionnaires

# script test 
# print(get_city())