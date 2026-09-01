from playwright.sync_api import sync_playwright
from urllib.parse import quote_plus
import time # temporisation
import random
from bs4 import BeautifulSoup
import pandas as pd
import re
import json
import cities_list
from utilities_tools_store import get_text
import cities_list

##### Script tests ####
# city = "Nice"
# checkin = "2026-09-10"
# checkout = "2026-09-11"
#######################


def get_hotel_info(city, checkin, checkout):
    """
    Récupère les informations des hôtels pour une ville donnée en utilisant le site Booking.com via Playwright.
    """

    city_url = quote_plus(city)

    url = f"https://www.booking.com/searchresults.fr.html?ss={city_url}&lang=fr&checkin={checkin}&checkout={checkout}"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        page = browser.new_page(
                viewport={"width": 1280, "height": 800},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                )

        page.goto(url,
            wait_until="domcontentloaded",
            timeout=30000
        )

        page.wait_for_load_state("networkidle")
        time.sleep(random.uniform(3, 6)) 

        
        hotel_cards = page.locator("div[data-testid='property-card']")

        hotel_cards.first.wait_for(
            state="visible",
            timeout=30000
        )
        # print(f"Nombre d'hôtels trouvés : {hotel_cards.count()}")
        
        city_text = page.locator("h1").inner_text()
        city = city_text.split(":")[0].strip().replace("-", " ")

        hotel_info = {"city" : city, "hotels": []}
        for i in range(hotel_cards.count()):
            card = hotel_cards.nth(i)

            name = get_text(card, "div[data-testid='title']")
            price = get_text(card, "span[data-testid='price-and-discounted-price']")
            score = get_text(card, "div[data-testid='review-score']")
            hotel_city = get_text(card, "span[data-testid='address-link']")
            #print(f"city: {city}, hotel city: {hotel_city}")

            hotel_info["hotels"].append({"hotel_city": hotel_city, "name": name, "price": price, "score": score})
            #print(f"Nom de l'hôtel : Ville : {name_city}, {name}, Prix : {price}, Score : {score}")

        browser.close()

    # with open("data/tests/hotel_info_test.json", "w", encoding="utf-8") as fichier:
    #     json.dump(
    #         hotel_info,
    #         fichier,
    #         ensure_ascii=False,
    #         indent=4
    #     )

    return hotel_info

##### script tests ####
# hotel_info = get_hotel_info(city, checkin, checkout)

# # print(hotel_info)
# print(len(hotel_info))
# print(type(hotel_info))
# with open("data/tests/hotel_info_test.json", "w", encoding="utf-8") as fichier:
#         json.dump(
#             hotel_info,
#             fichier,
#             ensure_ascii=False,
#             indent=4
#         )
#######################