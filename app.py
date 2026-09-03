# Ochestrateur de la recherche

from get_weather import get_weather_info, weather_call_response_test
from get_hotels import get_hotel_info
from get_cities import get_city_info, nominatim_call_response_test

from cities_list import cities_normalized, exercice_cities, booking_city_aliases, exercice_cities_booking_aliases, test_cities
from utilities_tools_store import standardize_city_text, get_text 

import time
import pandas as pd
import random
import traceback
import requests
import unicodedata

cities = exercice_cities # Liste des villes à traiter
# cities_standardized = [standardize_city_text(city) for city in cities]

checkin = "2026-09-10"
checkout = "2026-09-12"

# ----------------- Bloc de récupération des informations via l'API Nominatim pour toutes les villes de la liste cities. -----------------  #
#### Call api nominatim test ####
print("---------------------------------------------------------------------")
print("Récupération des informations géographiques pour toutes les villes...")
nominatim_call_response_test("France") # Vérifie le code de réponse de l'API Nominatim pour la France

##### Call api nominatim - Sortie => dataframe ####

cities_infos = get_city_info(cities)
print()
print(f"Nombre de villes récupérées sur nominatim : {len(cities_infos)}")
print("---------------------------------------------------------------------")

# ----------------- Bloc de récupération des informations via l'API OpenWeatherMap pour toutes les villes de la liste cities. -----------------  # 
print("---------------------------------------------------------------------")
print("Récupération des informations météo pour toutes les villes...")
##### Call api openweathermap test ####
weather_call_response_test("43.5661521", "4.19154") 

##### Call api openweathermap - Sortie => dataframe ####
weather_infos = get_weather_info(cities_infos)
print()
print(f"Nombre de villes récupérées sur openweathermap : {len(weather_infos)}")
print("---------------------------------------------------------------------")

# ----------------- Bloc de récupération des informations sur les hotels disponibles pour chaque ville de la liste cities. -----------------  #
print("---------------------------------------------------------------------")
print("Récupération des informations sur les hôtels pour toutes les villes...")
hotels_infos = []
failed_cities = []
for i, city in enumerate(exercice_cities_booking_aliases):
    try :
        print()
        print(f"Récupération des hôtels pour la ville : {city} ({i + 1}/{len(cities_infos)})...")
    
        hotel = get_hotel_info(city, checkin, checkout) # DataFrame des hôtels pour la ville actuelle

        if hotel is not None:
            hotel["city"] = city
            hotels_infos.append(hotel)
            print(f"Nombre d'hôtels trouvés pour {city} : {len(hotels_infos[-1]['hotels'])}")

        time.sleep(random.uniform(8, 12))  # Pause random entre chaque ville pour éviter de se faire exclure
        
        if (i + 1) % 20 == 0:
            print("Pause après 20 villes...")
            time.sleep(random.uniform(20, 30))  # Pause plus longue après chaque 20 villes
        
    except Exception as e:
        failed_cities.append(city)
        # hotels_infos["city"].append(city)  # Ajoute la ville à la liste des échecs pour référence
        print()
        if len(failed_cities) > 0:
            print(f"Aucun hôtel trouvé pour la ville : {city}")
            print(f"Villes en échec jusqu'à présent : {failed_cities}")
        print(f"Erreur : {e}")
        print()
        continue  # Passe à la ville suivante en cas d'erreur

for i, failed_city in enumerate(failed_cities):
    try : 
        print(f"Villes en échec ({i + 1}/{len(failed_cities)}) : {failed_city}")

        hotels_retry = get_hotel_info(failed_city, checkin, checkout)  # Retry pour les villes en échec
        if hotels_retry is not None:
            hotels_infos.append(hotels_retry)
            print(f"Nombre d'hôtels trouvés pour les villes : {failed_city} {len(hotels_retry['hotels'])}")
            time.sleep(random.uniform(8, 12))  # Pause random entre chaque ville pour éviter de se faire exclure
    except Exception as e:
        print(f"Erreur lors de la récupération des hôtels pour la ville en échec {failed_city} : {e}")
        
# ----------------- Bloc de création des DataFrames finaux -----------------  #
print("---------------------------------------------------------------------")
print("Création des DataFrames finaux...")
df_cities = cities_infos  # DataFrame final à partir de de la fonction get_city_info
df_cities = df_cities.rename(columns={"name": "city"})
df_weather = pd.DataFrame(weather_infos)
df_hotels = pd.DataFrame(hotels_infos) # Crée un DataFrame final à partir de la liste des DataFrames d'hôtels
df_hotels.to_csv("data/hotels_infos.csv", index=False, encoding="utf-8-sig") # Sauvegarde du DataFrame des hôtels en CSV

# Standardisation des noms de villes dans les DataFrames pour éviter les problèmes de fusion
df_cities["city"] = df_cities["city"].apply(standardize_city_text)
df_weather["city"] = df_weather["city"].apply(standardize_city_text)
df_hotels["city"] = df_hotels["city"].apply(standardize_city_text)


# region Vérification DataFrames avant merge

# print(f"type de df_cities : {type(df_cities)}")
# print(df_cities.head())
# print("------------------")

# print(f"type de df_weather : {type(df_weather)}")
# print(df_weather.head())
# print("------------------")

# print(f"type de df_hotels : {type(df_hotels)}")
# print(df_hotels.head())

# print("------------------")
# print("Colonnes villes :", df_cities.columns.tolist())
# print("Colonnes météo :", df_weather.columns.tolist())
# print("Colonnes hôtels :", df_hotels.columns.tolist())

# endregion

# ----------------- Bloc de fusion des DataFrames par ville -----------------  #

merge_cities_and_weather = pd.merge(df_cities, df_weather, left_on="city", right_on="city", how="right")  # Fusionne les deux DataFrames sur la colonne "city".
final_df = pd.merge(merge_cities_and_weather, df_hotels, left_on="city", right_on="city", how="right")  # Fusionne les deux DataFrames sur la colonne "city".
print("---------------------------------------------------------------------")
print(f"type de final_df : {type(final_df)}")
print(final_df.head())
print(f"Villes en échec : {failed_cities}")
print("---------------------------------------------------------------------")
print("---------------------------------------------------------------------")
# ----------------- Bloc de sauvegarde du DataFrame final en CSV -----------------  #
#final_df.to_csv("data/final_data_exercise_list.csv", index=False, encoding="utf-8-sig")
final_df.to_csv("data/tests/final_data.csv", index=False, encoding="utf-8-sig")