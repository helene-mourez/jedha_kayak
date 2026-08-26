
from playwright.sync_api import sync_playwright
import time # temporisation
import random
from bs4 import BeautifulSoup
import pandas as pd


url = "https://www.booking.com/searchresults.fr.html?ss=Saint-Malo&ssne=Saint-Malo&ssne_untouched=Saint-Malo&efdco=1&label=gen173nr-10CAEoggI46AdIM1gEaE2IAQGYATO4AQfIAQ3YAQPoAQH4AQGIAgGoAgG4Avu9sNQGwAIB0gIkZjZmYTY5ODgtMTU2MS00YmU5LTllNTMtMDQxNzNjM2VlZWQ02AIB4AIB&aid=304142&lang=fr&sb=1&src_elem=sb&src=index&dest_id=-1466824&dest_type=city&checkin=2026-08-24&checkout=2026-08-25&group_adults=2&no_rooms=1&group_children=0"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    page = browser.new_page(
            viewport={"width": 1280, "height": 800},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )

    page.goto(url,
        wait_until="domcontentloaded",
        timeout=60000
    )

    page.wait_for_load_state("networkidle")
    time.sleep(random.uniform(3, 6)) 

    
    hotel_cards = page.locator("div[data-testid='property-card']")

    hotel_cards.first.wait_for(
        state="visible",
        timeout=30000
    )
    print(f"Nombre d'hôtels trouvés : {hotel_cards.count()}")

    def get_text(card, selector):
        element = card.locator(selector)
        if element.count() == 0:
            return None
        return element.first.inner_text().strip()

    city_text = page.locator("h1").inner_text()

    city = city_text.split(":")[0].strip()

    print(city)