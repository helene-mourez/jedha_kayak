# import des librairies
import pandas as pd

from kayak_get_city import get_city
from kayak_get_weather import get_weather
# from kayak_get_current_weather import get_current_weather
# from kayak_get_hotel import get_hotel

# orchestration des fonctions call api get_city get_weather
cities_info=get_city()[0]
weather_info=get_weather(cities_info)[0]
# orchestration de la fonction scraping
# get_hotel=get_hotel()

# normalization dictionary list to dataframe
## cities
cities_df = pd.DataFrame(cities_info)

## weather
weather_df = pd.json_normalize(weather_info)
weather = pd.json_normalize(weather_df['weather'])
weather2 = pd.json_normalize(weather.to_dict(orient="records"))
weather2 = weather2.add_prefix("data.")

weather_df = pd.concat(
    [weather_df.drop(columns="weather"),
     weather2],
     axis=1)

# merge DataFrames on 'city'

current_weather = pd.merge(cities_df, weather_df, on='city')

# Display key columns
print("\nCurrent weather:")
current_weather.head()

print(current_weather)