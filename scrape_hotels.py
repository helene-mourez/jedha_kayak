from playwright.sync_api import sync_playwright
import time # temporisation
import random
from bs4 import BeautifulSoup

url = "https://www.booking.com/searchresults.fr.html?label=msn-8aGmFKcvjur7ORXD1T41Jg-80676853483926%3Atikwd-80677028168879%3Aloc-66%3Anes%3Amte%3Alp186792%3Adec%3Acid518941944%3Aagid1290827950458860%3Aclkida60dbefb136f17da04a9d47302b61cd6&aid=2369666&ss=Valensole&ssne=Valensole&ssne_untouched=Valensole&efdco=1&lang=fr&src=searchresults&dest_id=-1474456&dest_type=city&checkin=2026-08-21&checkout=2026-08-22&group_adults=2&no_rooms=1&group_children=0&nflt=distance%3D3000"
with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)

    page = browser.new_page(
            viewport={"width": 1280, "height": 800},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )

    page.goto(
        url,
        wait_until="domcontentloaded",
        timeout=60000
    )

    page.wait_for_load_state("networkidle")
    time.sleep(random.uniform(3, 6)) 

    html = page.content() 
    soup = BeautifulSoup(html, "html.parser")

    hotel_names = soup.find_all("div", {"data-testid": "title"})
    score_hotels = soup.find_all("div", {"data-testid": "review-score"})
    price_hotels = soup.find_all("span", {"data-testid": "price-and-discounted-price"})
    city = soup.find("h1", {"data-testid": "search-title"})
    


    for hotel, score, price in zip(hotel_names, score_hotels, price_hotels):
        print(f"Hotel: {hotel.text.strip()}, Score: {score.text.strip()}, Price: {price.text.strip()}, City: {city.text.strip()}")

    print(soup.title)
    print(hotel_names)

    # print(soup.content)
    # print(html[:500])

    browser.close()