from playwright.sync_api import sync_playwright
from urllib.parse import quote_plus
import time # temporisation
import random
from bs4 import BeautifulSoup
import pandas as pd
import re

##### Script tests ####
# city = "Saint-Malo"
#######################
checkin = "2026-08-28"
checkout = "2026-08-29"

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

        def get_text(card, selector):
            element = card.locator(selector)

            if element.count() == 0:
                return None

            text = BeautifulSoup(
                element.first.inner_text(),
                "html.parser"
            ).get_text(" ", strip=True)

            return re.sub(r"\s+", " ", text.replace("\xa0", " ")).strip()


        city_text = page.locator("h1").inner_text()
        city = city_text.split(":")[0].strip().replace("-", " ")

        hotel_info = {"city" : city, "hotels": []}
        for i in range(hotel_cards.count()):
            card = hotel_cards.nth(i)

            name = get_text(card, "div[data-testid='title']")
            price = get_text(card, "span[data-testid='price-and-discounted-price']")
            score = get_text(card, "div[data-testid='review-score']")

            hotel_info["hotels"].append({"name": name, "price": price, "score": score})
            #print(f"Nom de l'hôtel : Ville : {name_city}, {name}, Prix : {price}, Score : {score}")

        browser.close()

    #return pd.DataFrame(hotel_info)
    return hotel_info

##### script tests ####
# get_hotel = get_hotel_info(city, checkin, checkout)

# print(get_hotel)
# print (len(get_hotel))
# print(type(get_hotel))

# get_hotel.to_csv("data/hotels_scrap_test.csv", index=False, encoding="utf-8-sig")
#######################