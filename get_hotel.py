###get_hotel###

# import libraries

from playwright.sync_api import sync_playwright
from urllib.parse import quote_plus
import time # temporisation
import random
from bs4 import BeautifulSoup
import pandas as pd
import re
import json

##### Script tests ####
# city = "Saint-Malo"
# checkin = "2026-08-28"
# checkout = "2026-08-29"
#######################

def get_hotel(city, checkin, checkout):
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
        # # Trouver la suggestion qui commence par le nom de la ville
        # suggestions = page.locator("a[data-testid='suggested-destination']")
        # if suggestions.count() > 0:
        #     for i in range(suggestions.count()):
        #         text = suggestions.nth(i).inner_text()
        #         if text.lower().startswith(city.lower()):
        #             suggestions.nth(i).click()
        #             page.wait_for_load_state("networkidle")
        #             break    
        
        print(f"Nombre d'hôtels trouvés : {hotel_cards.count()}")


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

            # button = card.locator("button:has-text('Voir les disponibilités')")
            # button.click()
            # page.wait_for_load_state("networkidle")
            
            # # Scrapez les éléments de la 2e page ici
            # points forts
            strengths_list = page.locator("xpath=/html/body/div[4]/div/div[4]/main/div[1]/div[3]/div/div[1]/div[2]/div[2]/div/div/ul")
            strengths = strengths_list.locator("li")
            strengths_text = [strengths.nth(j).inner_text() for j in range(strengths.count())]
            
            # page.go_back()
            # hotel_cards = page.locator("div[data-testid='property-card']")

            hotel_info["hotels"].append({"name": name, "price": price, "score": score})
            # print(f"get_hotel : {hotel_info}")
            # print(f"ville : {city}, nom de l'hôtel : {name}, prix : {price}, score : {score}")        

        browser.close()

        return hotel_info

##### script tests ####
# get_hotel = get_hotel(city, checkin, checkout)

# print(get_hotel)
# print (len(get_hotel))
# print(type(get_hotel))
#######################