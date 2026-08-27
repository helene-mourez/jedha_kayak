# import libraries

import json
import time
import os

import requests
from dotenv import load_dotenv
import pandas as pd
from kayak_get_city import get_city

# V2.5 https://api.openweathermap.org/data/2.5/weather
# V4.0 https://api.openweathermap.org/data/4.0/onecall/current

def get_weather(cities_info):
    load_dotenv()
    weather_url = "https://api.openweathermap.org/data/2.5/weather"

    weather_info = []
    response = []
    
    for city in cities_info:
        try:
            params = {
                "lat": city['lat'], 
                "lon": city['lon'], 
                "units": "metric", 
                "appid": os.getenv("API_KEY")
                }

            weather_response = requests.get(weather_url, params=params)
            if weather_response.status_code==200 :
                response.append(200) # compteur status code = 200 sur les appels
            weather = weather_response.json()
            weather['city'] = city['city'] #weather_info.append({"city": city["city"], "weather": weather_response.json()})
            weather_info.append(weather)

        except (IndexError, KeyError, requests.exceptions.RequestException):
            print(f"Failed on {city} : {weather_response.status_code}")
        time.sleep(2)

    return weather_info, print(len(response))


##### script tests ####
if __name__ == "__main__": # ce test s'exécute seulement si le fichier est lancé directement
    cities_info = get_city()
    print(get_weather())