###app###
# import libraries

import pandas as pd

from playwright._impl._errors import TimeoutError
from datetime import date, timedelta
import re
import time 
import random
from config import cities, weather_url
from get_city import get_city
from get_weather import get_weather
import treatment as t
from get_hotel import get_hotel

# orchestration 

# call api 
## get_city 

cities_info = get_city(cities) # in dictionaries list, fetch per element
cities_df = t.cities_normalize(cities_info)

## get_weather

weather_url = weather_url

weather_info = get_weather(cities_info)[0]
weather_df = t.weather_normalize(weather_info)

# treat data
## normalize cities and weather

cities_df = t.cities_normalize(cities_info)
weather_df = t.weather_normalize(weather_info)

# merge DataFrames on 'city'
## merge city and weather 

current_weather_df = t.merge1(cities_df, weather_df)

# scrap hotel

hotel_info = []
no_hotel = []

checkin = date.today().strftime("%Y-%m-%d") 
checkout = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d") # tomorrow dates au format AAAA-MM-DD

# checkin = date.today().strftime("%Y-%m-%d") 
# checkout = (date.today() + timedelta(days=1)).strftime("%Y-%m-%d") # tomorrow dates au format AAAA-MM-DD

for i, city in enumerate(current_weather_df['city']):
    try :
        time.sleep(random.uniform(8, 12))  # Pause random entre chaque ville pour éviter de se faire exclure

        hotel = get_hotel(city, checkin, checkout) # DataFrame des hôtels pour la ville actuelle

        if hotel['hotels']:
            hotel['city'] = city
            hotel_info.append(hotel)
        else :
            no_hotel.append(city)
        print(f"{len(hotel['hotels'])} hotel(s) found in {city}")

        if (i + 1) % 20 == 0:
            print("Pause after 20 cities...")
            time.sleep(random.uniform(30, 60))  # Pause plus longue après chaque 20 villes

    except Exception as e:
        print(f"No hotel fetched : {city}")
        print(f"Technical error : {e}")
        continue  # Passe à la ville suivante en cas d'erreur   
   
## normalize hotel

hotel_df = t.hotel_normalize(hotel_info)

## merge DataFrames current weather per city and hotel on 'city' 

df = t.merge2(current_weather_df, hotel_df)
print(f"No hotel available today : {len(no_hotel)} in {no_hotel}")

print(hotel_df)
# print(df)

# write csv file 

df.to_csv("data\merged_data.csv", index=False) # avoid a second index creation