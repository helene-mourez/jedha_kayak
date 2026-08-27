# import libraries

import pandas as pd

from kayak_get_city import get_city
from kayak_get_weather import get_weather
import kayak_treatment as t
from kayak_get_hotel import get_hotel
from playwright._impl._errors import TimeoutError

from datetime import date, timedelta
import re
import time 
import random

# orchestration 

# call api 
## get_city 

cities = [# "Aigues Mortes", "Aix en Provence", "Amiens", "Annecy", "Avignon",
    # "Barjols", "Bayeux", "Bayonne", "Besancon", "Biarritz", 
	# "Bormes les Mimosas", "Bédeilhac-et-Aynat", "Camon", "Carcassonne", 
	"Carla-Bayle", # "Cassis", "Castellane", "Collioure", "Colmar", "Cotignac",
    # "Dijon", "Eguisheim", "Foix", "Grenoble", "La Rochelle", "Le Havre",
    "Le Mas-d’Azil",# "Lille", "Lyon", "Marseille", "Mirepoix", 
	# "Mont Saint Michel", "Montauban", "Montségur", "Moustiers-Sainte-Marie",
    # "Niaux", "Nimes", "Orschwiller", "Paris", "Rouen", "Saint-Lizier",
    "Saint-Martin-d’Oydes",# "Sainte-Croix-du-Verdon", 
	# "Saintes Maries de la mer", "Sillans-la-Cascade", "St Malo", "Strasbourg",
    # "Tarascon-sur-Ariège", "Toulouse", "Uzes", 
    "Valensole"
    ]
cities_info = get_city(cities) # in dictionaries list, fetch per element
cities_df = t.cities_normalize(cities_info)

## get_weather

weather_info = get_weather(cities_info)[0]
weather_df = t.weather_normalize(weather_info)

# treat data
## normalize

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

for i, city in enumerate(current_weather_df['city']):
    try :
        time.sleep(random.uniform(8, 12))  # Pause random entre chaque ville pour éviter de se faire exclure

        hotel = get_hotel(city, checkin, checkout) # DataFrame des hôtels pour la ville actuelle

        if hotel is not None:
            hotel["city"] = city
            hotel_info.append(hotel)
            print(f"Nombre d'hôtels trouvés pour {city} : {len(hotel_info[-1]['hotels'])}")
        else :
            no_hotel.append(city)

        if (i + 1) % 20 == 0:
            print("Pause après 20 villes...")
            time.sleep(random.uniform(30, 60))  # Pause plus longue après chaque 20 villes

    except Exception as e:
        print(f"Aucun hôtel disponible : {city}")
        print(f"Villes en échec : {no_hotel}")
        print(f"Erreur : {e}")
        continue  # Passe à la ville suivante en cas d'erreur   
   
hotel_df = t.hotel_normalize(hotel_info)

## merge DataFrames current weather per city and hotel on 'city' 

df = t.merge2(current_weather_df, hotel_df)

print(hotel_df)
print(df)

# write csv file 

df.to_csv("current_weather_cities_hotel.csv", index=False) # avoid a second index creation

# open csv file

# f = {'file': open('current_weather_cities_hotel.csv', 'rb')} # rb = binary mode avoids encodage errors

# pd.read_csv("current_weather_cities_hotel.csv")

# verify gps coordinates of all the cities

# import plotly.express as px
# import plotly.io as pio

# pio.renderers.default = "notebook"

# create map using Plotly

# fig = px.scatter_map(
#     df,
#     lat="lat",
#     lon="lon",
#     hover_name="name",
#     hover_data={
#         "lat": False, "lon": False
#     },
#     color_discrete_sequence=["blue"],
#     zoom=5,
# )

# # Configure the map layout
# fig.update_layout(
#     map_style="open-street-map",
#     margin={"r":0,"t":0,"l":0,"b":0}
# )

# fig.show()