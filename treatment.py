###treatment###
# import libraries
import pandas as pd
import json

from get_city import get_city
from get_weather import get_weather

# call api get_city get weather

# cities_info=get_city()[0] # arguments in dictionaries list, fetch per element
# weather_info=get_weather(cities_info)[0]

# normalization dictionary list to dataframe
## cities

def cities_normalize(cities_info):
    cities_df = pd.DataFrame(cities_info)
    cities_df.to_csv("data\cities.csv", index=False)
    return cities_df

## weather

def weather_normalize(weather_info):
    weather_df = pd.json_normalize(weather_info)
    weather = pd.json_normalize(weather_df['weather'])
    weather2 = pd.json_normalize(weather.to_dict(orient="records"))
    weather2 = weather2.add_prefix("data.")

    weather_df = pd.concat([
        weather_df.drop(columns="weather"),
        weather2
        ],axis=1)
    weather_df.to_csv("data\weather.csv", index=False)
    return weather_df 

# hotel

# à refaire en tenant compte de hotel_city
def hotel_normalize(hotel_info):
    hotel = [h for city in hotel_info for h in city] 
    hotel_df = pd.json_normalize(hotel_info)
    # normalize dataframe and add city for each hotel
    hotel = [{**h, 'city': item['city']} 
             for item in hotel_info 
             for h in item['hotels']] 
    hotel_df = pd.json_normalize(hotel)
    # add prefix column hotel.
    hotel_df = hotel_df.rename(columns={
        'name': 'hotel.name', 'price': 'hotel.price', 'score': 'hotel.score'
    })
    # extract data from hotel.name et hotel.score
    hotel_df['hotel.label'] = hotel_df['hotel.name'].str.split(' - ').str[0] # register hotel label
    hotel_df['hotel.rate'] = hotel_df['hotel.score'].str.extract(r'(?:de\s+)?(\d+(?:,\d+)?)') # extract hotel score  
    hotel_df['hotel.rate_label'] = hotel_df['hotel.score'].str.extract(r'(?:\d+(?:,\d+)?)\s+(?:\d+(?:,\d+)?)\s+([^\d]+?)\s+\d+')[0].str.strip() # extract rate label
    hotel_df['hotel.experience'] = hotel_df['hotel.score'].str.extract(r'(\d+(?:\s+\d+)*)\s+expériences') # extract rental number of the client
    hotel_df = hotel_df.drop(columns=['hotel.name', 'hotel.score'])
    hotel_df.to_csv("data\hotel.csv", index=False)
    return hotel_df

# merge DataFrames on city
##  cities_info and weather_info for current_weather per cities

def merge1(cities_df, weather_df): 
    current_weather_df = pd.merge(cities_df, weather_df, on='city')

    # force some values on booking.com
    mapping = {"Le Carla-Bayle" : "Carla-Bayle",              
                "Saintes-Maries-de-la-Mer" : "Les Saintes-Maries-de-la-Mer, Provence-Alpes-Côte d'Azur (Sud de la France), France"} 
    current_weather_df["city"] = current_weather_df["city"].replace(mapping) 
    # print(f"***clean_cities*** : {current_weather_df['city'].tolist()}")
    return current_weather_df

##  current_weather and hotel_info for weather per hotel

def merge2(current_weather_df, hotel_df):
    df = pd.merge(current_weather_df, hotel_df, on='city')
    return df