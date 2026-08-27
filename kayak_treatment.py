# import libraries
import pandas as pd
import json

from kayak_get_city import get_city
from kayak_get_weather import get_weather

# call api get_city get weather

# cities_info=get_city()[0] # arguments in dictionaries list, fetch per element
# weather_info=get_weather(cities_info)[0]

# normalization dictionary list to dataframe
## cities

def cities_normalize(cities_info):
    cities_df = pd.DataFrame(cities_info)
    return cities_df

## weather

def weather_normalize(weather_info):
    weather_df = pd.json_normalize(weather_info)
    weather = pd.json_normalize(weather_df['weather'])
    weather2 = pd.json_normalize(weather.to_dict(orient="records"))
    weather2 = weather2.add_prefix("data.")

    weather_df = pd.concat(
        [weather_df.drop(columns="weather"),
        weather2],
        axis=1)
    return weather_df 

# hotel

def hotel_normalize(hotel_info):
    hotel_df = pd.DataFrame(hotel_info)
    return hotel_df

# merge DataFrames on city
##  cities_info and weather_info for current_weather per cities

def merge1(cities_df, weather_df): 
    current_weather_df = pd.merge(cities_df, weather_df, on='city')

    mapping = {"Le Carla-Bayle" : "Carla-Bayle",
                    "Le Mas-d'Azil" : "Le Mas-d'Azil, D119, 09290", # Le Mas-d'Azil, Le Mas-d'Azil, Occitanie, France
                    "Saint-Martin-d'Oydes" : "Saint-Martin-d'Oydes, Saint-Martin-d'Oydes, Occitanie", # Saint-Martin-d'Oydes, D626 A, 09100
                    "Saintes-Maries-de-la-Mer" : "Les Saintes-Maries-de-la-Mer, Provence-Alpes-Côte d'Azur (Sud de la France), France"} 
    current_weather_df["city"] = current_weather_df["city"].replace(mapping) # force some values on booking.com
    # print(f"***clean_cities*** : {current_weather_df['city'].tolist()}")
    return current_weather_df

##  current_weather and hotel_info for weather per hotel

def merge2(current_weather_df, hotel_df):
    df = pd.merge(current_weather_df, hotel_df, on='city')
    return df