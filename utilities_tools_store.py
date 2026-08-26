# Bibliothèques de fonctions utilitaires pour le projet

import unicodedata

# standardisation des noms de villes pour le merge
def standardize_city_text(city):
    city = city.lower()
    city = unicodedata.normalize("NFKD", city)
    city = "".join(c for c in city if not unicodedata.combining(c))
    city = city.replace("-", " ")
    city = city.replace("'", " ")
    city = city.replace("’", " ")
    city = " ".join(city.split())
    return city

# fonction de récupération du texte d'un élément HTML en utilisant BeautifulSoup et Playwright
from bs4 import BeautifulSoup
import re
def get_text(card, selector):
            element = card.locator(selector)

            if element.count() == 0:
                return None

            text = BeautifulSoup(
                element.first.inner_text(),
                "html.parser"
            ).get_text(" ", strip=True)

            return re.sub(r"\s+", " ", text.replace("\xa0", " ")).strip()
