#pip install playwright` 
# playwright install`
from playwright.sync_api import sync_playwright
import time # temporisation
import random
from bs4 import BeautifulSoup

url = "https://www.booking.com/searchresults.fr.html?label=msn-8aGmFKcvjur7ORXD1T41Jg-80676853483926%3Atikwd-80677028168879%3Aloc-66%3Anes%3Amte%3Alp186792%3Adec%3Acid518941944%3Aagid1290827950458860%3Aclkida60dbefb136f17da04a9d47302b61cd6&aid=2369666&ss=Valensole&ssne=Valensole&ssne_untouched=Valensole&efdco=1&lang=fr&src=searchresults&dest_id=-1474456&dest_type=city&checkin=2026-08-21&checkout=2026-08-22&group_adults=2&no_rooms=1&group_children=0&nflt=distance%3D3000"

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False) # réglage anti détection
    page = browser.new_page(
        viewport={"width": 1280, "height": 800},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
    page.goto(url)
    page.wait_for_load_state("networkidle")
    time.sleep(random.uniform(3, 6)) # tempo aléatoire
    html = page.content() 
    soup = BeautifulSoup(html, "html.parser")

    # hotel cards
    cards = soup.find_all("div", {"data-testid": "property-card"})
    for card in cards:
        nom = card.find("div", {"data-testid": "title"})
        prix = card.find("span", {"data-testid": "price-and-discounted-price"})
        note = card.find("div", {"data-testid": "review-score"})
        adresse = card.find("span", {"data-testid": "address-link"})
        lien = card.find("a", {"data-testid": "title-link"})
        print(nom.text.strip() if nom else None)
        print(prix.text.strip() if prix else None)
        print(note.text.strip() if note else None)
        print(adresse.text.strip() if adresse else None)
        print(lien["href"] if lien else None)
    


    print(len(cards))
    #print(soup.title)    #print(html[:500])
    browser.close()

    ''' # hotels names
    hotel_names = soup.find_all("div", {"data-testid": "title"})
    for hotel in hotel_names:
        print(hotel.text.strip())

    # hotels prices
    prices = soup.find_all("span", {"data-testid": "price-and-discounted-price"})
    for price in prices:
        print(price.text.strip())'''