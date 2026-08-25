import requests
import json
import time
from dotenv import load_dotenv
import os
import pandas as pd
from kayak_get_city import get_city
load_dotenv()

# V2.5 https://api.openweathermap.org/data/2.5/weather
# V4.0 https://api.openweathermap.org/data/4.0/onecall/current

# script test get_weather() function argument
# cities_info = get_city()[0]

def get_weather(cities_info):
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
            print(f"Execution with errors for {city} : {weather_response.status_code}")
        time.sleep(2)

    return weather_info, print(len(response))

# script test 
# print(get_weather(cities_info))