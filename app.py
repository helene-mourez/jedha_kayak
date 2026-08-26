# Ochestrateur de la recherche

from get_weather import get_weather_info, weather_call_response_test
from get_hotels import get_hotel_info
from get_cities import get_city_info, nominatim_call_response_test
from cities_list import cities_normalized, exercice_cities

import time
import pandas as pd
import random
import traceback
import requests

# df_weather = get_weather_info()
cities = cities_normalized
checkin = "2026-08-28"
checkout = "2026-08-29"

# ----------------- Bloc de récupération des informations via l'API Nominatim pour toutes les villes de la liste cities. -----------------  #

#### Call api nominatim test ####
nominatim_call_response_test("France") # Vérifie le code de réponse de l'API Nominatim pour la France

##### Call api nominatim - Sortie => dataframe ####
cities_infos = get_city_info(cities) 
    
# ----------------- Bloc de récupération des informations via l'API OpenWeatherMap pour toutes les villes de la liste cities. -----------------  #
    
##### Call api openweathermap test ####
weather_call_response_test("43.5661521", "4.19154") 

##### Call api openweathermap - Sortie => dataframe ####
print("Récupération des informations météo pour toutes les villes...")
weather_infos = get_weather_info(cities_infos)

# ----------------- Bloc de récupération des informations sur les hotels disponibles pour chaque ville de la liste cities. -----------------  #

hotels_infos = []
failed_cities = []
for i, city in enumerate(cities):
    try : 
        print(f"Récupération des hôtels pour la ville : {city} ({i + 1}/{len(cities)})...")
    
        hotel = get_hotel_info(city, checkin, checkout) # DataFrame des hôtels pour la ville actuelle

        if hotel is not None:
            hotels_infos.append(hotel)
            print(f"Nombre d'hôtels trouvés pour {city} : {len(hotels_infos[-1]['hotels'])}")
        else :
            failed_cities.append(city)

        # time.sleep(random.uniform(8, 12))  # Pause random entre chaque ville pour éviter de se faire exclure
        
        if (i + 1) % 20 == 0:
            print("Pause après 20 villes...")
            time.sleep(random.uniform(30, 60))  # Pause plus longue après chaque 20 villes
        

    except Exception as e:
        print(f"Aucun hôtel trouvé pour la ville : {city}")
        print(f"Erreur : {e}")
        continue  # Passe à la ville suivante en cas d'erreur

###############
# ATTENTION !!! Hélène : il faut que tu ajoute ton applatissement pour le df_weather et le df_city, les miens sont fait dans leurs dépendances. 
###############

print("Création des DataFrames finaux...")
df_cities = cities_infos  # DataFrame final à partir de de la fonction get_city_info
df_cities = df_cities.rename(columns={"name": "city"})
df_weather = pd.DataFrame(weather_infos)
df_hotels = pd.DataFrame(hotels_infos) # Crée un DataFrame final à partir de la liste des DataFrames d'hôtels

############## Prints de vérification de la structure des DataFrames (À faire AVANT de merger) #################
# print(f"type de df_cities : {type(df_cities)}")
# print(df_cities.head())
# print("------------------")
# df_weather = df_weather.drop(columns=["city"], errors="ignore")
# df_weather = df_weather.rename(columns={"name": "city"})
# print(f"type de df_weather : {type(df_weather)}")
# print(df_weather.head())
# print("------------------")
# print(f"type de df_hotels : {type(df_hotels)}")
# print(df_hotels.head())
# print("------------------")
# print("Colonnes villes :", df_cities.columns.tolist())
# print("Colonnes météo :", df_weather["city"])
# print("Colonnes hôtels :", df_hotels.columns.tolist())
# --------------------------------------------------------------------------------------- #

merge_cities_and_weather = pd.merge(df_cities, df_weather, left_on="city", right_on="city", how="right")  # Fusionne les deux DataFrames sur la colonne "city".
final_df = pd.merge(merge_cities_and_weather, df_hotels, left_on="city", right_on="city", how="right")  # Fusionne les deux DataFrames sur la colonne "city".

print(f"type de final_df : {type(final_df)}")
print(final_df.head())

final_df.to_csv("data/final_data.csv", index=False, encoding="utf-8-sig")