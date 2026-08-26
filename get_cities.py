import requests
import pandas as pd
from unidecode import unidecode
import time
import traceback
from cities_list import cities_normalized, exercice_cities


def nominatim_call_response_test(country):
    """
    Test the response of the Nominatim API call.
    """
    url = "https://nominatim.openstreetmap.org/search"
    
    params = {
        "country": country,
        "format": "geocodejson"
    }
    headers = {"User-Agent": "projet_etude_dataviz (lnmourez@gmail.com)"}
    response = requests.get(url, params=params, headers=headers) # call api

    return print(f"status code du call api nominatim : {response.status_code}")

def get_city_info(cities):
    """
    Get city information as name, place_id, latitude and longitude from the Nominatim API for a list of cities
    """

    url = "https://nominatim.openstreetmap.org/search"
    headers = {"User-Agent": "projet_etude_dataviz (lnmourez@gmail.com)"}

    rows = []
    for city in cities:
        params = {"q": city, "format": "geocodejson", "countrycodes": "fr"}
        response = requests.get(url, params=params, headers=headers)
        response_json = response.json()

        if response_json["features"]:
            features_response = response_json["features"][0] # takes only the first entry
            rows.append({
                "name": features_response["properties"]["geocoding"]["name"], # name is the attribute for cities which would be deplicated
                "place_id": features_response["properties"]["geocoding"]["place_id"],
                "lat": features_response["geometry"]["coordinates"][1],
                "lon": features_response["geometry"]["coordinates"][0]
            })
        else :
            print(f"City not found: {city}")
            print(f"error : {response_json}")
            traceback.print_exc()
            rows.append({
                "name": city,
                "place_id": None,
                "lat": None,
                "lon": None
            })
        time.sleep(1) 

    cities_infos = pd.DataFrame(rows)

    # drop coma and dash on name column
    cities_infos["name"] = cities_infos["name"].str.replace(r"[,\-]", " ", regex=True)
    # drop accents on name column
    cities_infos["name"] = cities_infos["name"].apply(unidecode)

    return cities_infos

###### script tests ####
# cities = cities_normalized
# cities_infos = get_city_info(cities)
# print(cities_infos)
# Writing a file
# cities_infos.to_csv("data/cities_test.csv", index=False) # avoid a second index creation