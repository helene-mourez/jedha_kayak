from playwright.sync_api import sync_playwright, Page
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from urllib.parse import quote_plus, urljoin
import time # temporisation
import random
from bs4 import BeautifulSoup
import pandas as pd
import re
import json
import cities_list
from utilities_tools_store import get_text
import cities_list
from typing import TypedDict

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

        context = browser.new_context(
                viewport={"width": 1280, "height": 800},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
                )
        page = context.new_page()
        detail_page = context.new_page()

        page.goto(url,
            wait_until="domcontentloaded",
            timeout=30000
        )

        page.wait_for_load_state("networkidle")
        time.sleep(random.uniform(3, 6)) 

        
        hotel_cards = page.locator("div[data-testid='property-card']")

        hotel_cards.first.wait_for(
            state="visible",
            timeout=60000
        )
        
        city_text = page.locator("h1").inner_text()
        city = city_text.split(":")[0].strip().replace("-", " ")

        hotel_info = {"city" : city, "hotels": []}
        for i in range(hotel_cards.count()):
            card = hotel_cards.nth(i)

            name = get_text(card, "div[data-testid='title']")
            price = get_text(card, "span[data-testid='price-and-discounted-price']")
            score = get_text(card, "div[data-testid='review-score']")
            hotel_city = get_text(card, "span[data-testid='address-link']")

            # Récupération de l'URL de l'hôtel et des coordonnées géographiques
            relative_url = card.locator("a[data-testid='title-link']").first.get_attribute("href")
            if relative_url is None:
                raise RuntimeError(f"Booking URL not found for {name}")

            hotel_url = urljoin(page.url, relative_url)

            detail_page.goto(
                hotel_url,
                wait_until="domcontentloaded",
                timeout=30_000,
            )

            try: 
                lat_lon = detail_page.locator("xpath=(//*[@data-atlas-latlng])[1]").get_attribute(
                    "data-atlas-latlng",
                    timeout=10_000,
                )
            except PlaywrightTimeoutError as exc:
                raise RuntimeError(f"Coordonnées non trouvées pour {name}") from exc
            # c'est pas un doublon avec le try except ? 
            if lat_lon is None:
                raise RuntimeError(f"Coordonnées non trouvées pour {name}")
            # -----
            latitude_text, longitude_text = lat_lon.split(",", maxsplit=1)
            latitude = float(latitude_text)
            longitude = float(longitude_text)

            ### Hélène : Bloc de récupration des sous notes :
            # try : 
            #     sous_notes = detail_page.locator("xpath= - xpath-des-sous notes/sous notes").get_attribute(
            #                         "data-atlas-latlng",
            #                         timeout=10_000,
            #                     )
            #     except PlaywrightTimeoutError as exc:
            #         raise RuntimeError(f"Sous notes non trouvées pour {name}") from exc

            # traitement des sous notes pour les ajouter à l'info de l'hôtel
            # ...

            hotel_info["hotels"].append({"hotel_city": hotel_city, "name": name, "price": price, "score": score, "latitude": latitude, "longitude": longitude, }) #"sous_notes": sous_notes})

        detail_page.close()
        context.close()
        browser.close()

    # rwith open("data/tests/hotel_info_test.json", "w", encoding="utf-8") as fichier:
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