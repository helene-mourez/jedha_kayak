import requests
import pandas as pd
from unidecode import unidecode
import time

def weather_call_response_test(lat, lon):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
            "lat": lat,
            "lon": lon,
            "units": "metric",
            "appid": "95f5ed4b5991c2bd754589456f14cc16",
            "lang": "fr"
        }
    response = requests.get(url, params=params) # Call api openweathermap test
    return print(f"status code du call api openweathermap : {response.status_code}") # check if the call is successful

def get_weather_info(cities_infos):
    """
    Récupère les informations météo pour une liste de villes en utilisant l'API OpenWeatherMap.
    """
    url = "https://api.openweathermap.org/data/2.5/weather"

    rows = []
    for _, row in cities_infos.iterrows():
        params = {
            "lat": row["lat"],
            "lon": row["lon"],
            "units": "metric",
            "appid": "95f5ed4b5991c2bd754589456f14cc16",
            "lang": "fr"
        }
        response = requests.get(url, params=params) # Call api

        payload = response.json()
        payload["city"] = row["name"]

        rows.append(payload)

        time.sleep(1)

    

    df_rows = pd.DataFrame(rows)
    #print(df_rows)

    # Applatissement général du JSON
    df_weather = pd.json_normalize(rows)

    # Applatissement du JSON pour la colonne "weather"
    weather = pd.json_normalize(df_rows["weather"])
    final_weather = pd.json_normalize(weather.to_dict(orient="records"))
    final_weather = final_weather.add_prefix("weather.")

    df_weather = pd.concat(
        [
            df_weather.drop(columns="weather"),
            final_weather
        ],
        axis=1
    )
    df_weather.to_csv("data/cities_and_weather_test.csv", index=False, encoding="utf-8-sig")
    return df_weather


##### script tests ####
# df_weather = get_weather_info()

# print(df_weather)
# print (len(df_weather))
# print(type(df_weather))

# df_weather.to_csv("data/cities_and_weather_test.csv", index=False, encoding="utf-8-sig")
#######################