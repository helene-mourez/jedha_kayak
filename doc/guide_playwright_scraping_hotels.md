# Guide minimal --- Scraper des résultats d'hôtels avec Playwright (Python)

> **Objectif pédagogique :** partir de zéro avec Playwright, ouvrir une
> page de résultats, extraire quelques informations visibles sur les
> hôtels, puis produire un fichier CSV exploitable avec pandas.
>
> **Important :** Booking.com indique actuellement dans ses conditions
> que le scraping/crawling automatisé de sa plateforme n'est pas
> autorisé sans autorisation écrite préalable. Utilise donc ce guide
> uniquement dans le cadre autorisé par ton école / la plateforme
> ciblée. Le code reste volontairement générique : il n'essaie pas de
> contourner un CAPTCHA, un blocage ou une protection anti-bot.

------------------------------------------------------------------------

## 0. Pipeline que l'on va construire

``` text
liste de villes
    ↓
Playwright ouvre une page de résultats
    ↓
attente du chargement des cartes d’hôtels
    ↓
extraction :
- ville
- nom de l’hôtel
- prix (si présent)
- note (si présente)
- adresse / localisation (si présente)
- URL (si présente)
    ↓
liste de dictionnaires Python
    ↓
pandas.DataFrame
    ↓
hotels.csv
```

On ne construit **ni classe, ni base de données, ni architecture
complexe**. Un script Python suffit pour commencer.

------------------------------------------------------------------------

# 1. Installer les bibliothèques

Dans le terminal de VS Code, dans ton environnement Python :

``` bash
pip install playwright pandas
```

Puis installer Chromium utilisé par Playwright :

``` bash
playwright install chromium
```

Playwright pilote alors un vrai navigateur Chromium.

------------------------------------------------------------------------

# 2. Vérifier que Playwright fonctionne

Crée un fichier :

``` text
scrape_hotels.py
```

Commence par ce test minimal :

``` python
from playwright.sync_api import sync_playwright


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    page = browser.new_page()

    page.goto("https://example.com")

    print(page.title())

    browser.close()
```

Lance :

``` bash
python scrape_hotels.py
```

### À comprendre

``` python
sync_playwright()
```

démarre Playwright.

``` python
p.chromium.launch(...)
```

lance Chromium.

``` python
headless=False
```

permet de **voir le navigateur** pendant le développement.

``` python
page = browser.new_page()
```

ouvre un nouvel onglet.

``` python
page.goto(...)
```

navigue vers une URL.

Pendant le développement, garde `headless=False`. Quand tout fonctionne,
tu pourras passer à :

``` python
headless=True
```

------------------------------------------------------------------------

# 3. Ouvrir une page de résultats

Le principe est simplement :

``` python
page.goto(URL)
```

Par exemple :

``` python
url = "URL_DE_LA_PAGE_DE_RESULTATS"

page.goto(url)
```

Ajoute un timeout raisonnable :

``` python
page.goto(
    url,
    wait_until="domcontentloaded",
    timeout=60000
)
```

Cela signifie :

-   ouvrir l'URL ;
-   attendre que le DOM principal soit chargé ;
-   abandonner après 60 secondes si nécessaire.

------------------------------------------------------------------------

# 4. Comprendre les `locator`

Avec Scrapy, tu utilisais surtout CSS/XPath.

Playwright utilise principalement des **locators**.

Exemple :

``` python
hotels = page.locator("SELECTEUR_DES_CARTES_HOTELS")
```

Puis :

``` python
print(hotels.count())
```

pour connaître le nombre d'éléments trouvés.

Playwright accepte encore CSS et XPath :

``` python
page.locator("div.ma-classe")
```

ou :

``` python
page.locator("//div[@class='ma-classe']")
```

Mais quand c'est possible, Playwright recommande des sélecteurs plus
proches de ce que voit l'utilisateur (`get_by_role`, `get_by_text`,
etc.).

Pour du scraping d'une liste de cartes, un sélecteur CSS court et stable
reste souvent pratique.

------------------------------------------------------------------------

# 5. Trouver les bons éléments

Ouvre la page normalement dans ton navigateur.

Puis :

1.  clic droit sur une carte d'hôtel ;
2.  **Inspecter** ;
3.  cherche l'élément HTML qui représente une carte complète ;
4.  repère un attribut ou une classe suffisamment stable.

Tu veux arriver à quelque chose du type :

``` python
hotel_cards = page.locator("SELECTEUR_CARTE_HOTEL")
```

Puis teste :

``` python
print("Nombre de cartes :", hotel_cards.count())
```

Si tu vois par exemple :

``` text
Nombre de cartes : 25
```

tu as trouvé le bon niveau.

------------------------------------------------------------------------

# 6. Attendre que les hôtels soient chargés

Ne fais pas simplement :

``` python
page.goto(url)
hotel_cards = ...
```

car les résultats peuvent apparaître après le chargement initial.

Utilise :

``` python
hotel_cards = page.locator("SELECTEUR_CARTE_HOTEL")

hotel_cards.first.wait_for(
    state="visible",
    timeout=30000
)
```

Puis :

``` python
print(hotel_cards.count())
```

Playwright gère déjà beaucoup d'attentes automatiquement, ce qui est
l'un de ses gros avantages par rapport à un simple téléchargement HTML.

------------------------------------------------------------------------

# 7. Inspecter une seule carte avant de tout scraper

Avant de faire une boucle, travaille uniquement avec la première carte :

``` python
card = hotel_cards.nth(0)

print(card.inner_text())
```

Cela te permet de voir tout le texte visible de la carte.

Exemple fictif :

``` text
Hôtel Exemple
Paris
8,7
Très bien
125 €
```

À ce stade, ton objectif est de trouver séparément les éléments qui
t'intéressent.

------------------------------------------------------------------------

# 8. Extraire le nom d'un hôtel

Une fois le bon sous-élément identifié :

``` python
name = card.locator("SELECTEUR_NOM").inner_text()
```

Puis :

``` python
print(name)
```

Même logique pour les autres champs.

------------------------------------------------------------------------

# 9. Extraire plusieurs informations

Exemple générique :

``` python
name = card.locator("SELECTEUR_NOM").inner_text()
price = card.locator("SELECTEUR_PRIX").inner_text()
score = card.locator("SELECTEUR_NOTE").inner_text()
```

Mais attention : certains hôtels peuvent ne pas avoir tous les champs.

Une extraction directe peut donc provoquer une erreur.

On va régler ça simplement.

------------------------------------------------------------------------

# 10. Petite fonction pour les champs facultatifs

Ajoute :

``` python
def get_text(card, selector):
    element = card.locator(selector)

    if element.count() == 0:
        return None

    return element.first.inner_text().strip()
```

Tu peux maintenant écrire :

``` python
name = get_text(card, "SELECTEUR_NOM")
price = get_text(card, "SELECTEUR_PRIX")
score = get_text(card, "SELECTEUR_NOTE")
```

Si l'information n'existe pas :

``` python
None
```

sera enregistrée.

C'est beaucoup plus pratique pour construire ensuite le DataFrame.

------------------------------------------------------------------------

# 11. Récupérer une URL

Pour un lien :

``` python
link = card.locator("a").first.get_attribute("href")
```

Si le lien est dans un élément plus précis :

``` python
link = card.locator("SELECTEUR_LIEN").get_attribute("href")
```

------------------------------------------------------------------------

# 12. Boucler sur tous les hôtels

Une fois l'extraction validée sur **une seule carte**, seulement à ce
moment-là fais la boucle :

``` python
hotels_data = []

for i in range(hotel_cards.count()):

    card = hotel_cards.nth(i)

    hotel = {
        "name": get_text(card, "SELECTEUR_NOM"),
        "price": get_text(card, "SELECTEUR_PRIX"),
        "score": get_text(card, "SELECTEUR_NOTE"),
    }

    hotels_data.append(hotel)
```

Tu obtiens quelque chose comme :

``` python
[
    {
        "name": "Hotel A",
        "price": "120 €",
        "score": "8.4"
    },
    {
        "name": "Hotel B",
        "price": "98 €",
        "score": "7.9"
    }
]
```

------------------------------------------------------------------------

# 13. Ajouter la ville

Comme tu devras ensuite joindre les hôtels aux données météo, **garde
impérativement la ville dans chaque ligne**.

``` python
city = "Paris"
```

Puis :

``` python
hotel = {
    "city": city,
    "name": get_text(card, "SELECTEUR_NOM"),
    "price": get_text(card, "SELECTEUR_PRIX"),
    "score": get_text(card, "SELECTEUR_NOTE"),
}
```

Ton CSV pourra alors ressembler à :

``` text
city,name,price,score
Paris,Hotel A,120 €,8.4
Paris,Hotel B,98 €,7.9
```

La colonne `city` servira ensuite de clé pour la jointure avec tes
données météo / coordonnées.

------------------------------------------------------------------------

# 14. Passer à plusieurs villes

Quand **une ville fonctionne correctement**, transforme simplement la
logique en boucle.

``` python
cities = [
    "Paris",
    "Lyon",
    "Bordeaux"
]
```

Puis :

``` python
all_hotels = []

for city in cities:

    url = construire_url(city)

    page.goto(
        url,
        wait_until="domcontentloaded",
        timeout=60000
    )

    hotel_cards = page.locator("SELECTEUR_CARTE_HOTEL")

    hotel_cards.first.wait_for(
        state="visible",
        timeout=30000
    )

    for i in range(hotel_cards.count()):

        card = hotel_cards.nth(i)

        hotel = {
            "city": city,
            "name": get_text(card, "SELECTEUR_NOM"),
            "price": get_text(card, "SELECTEUR_PRIX"),
            "score": get_text(card, "SELECTEUR_NOTE"),
        }

        all_hotels.append(hotel)
```

**Ne commence pas directement avec les 35 villes.**

Ordre conseillé :

``` text
1 ville
↓
3 villes
↓
35 villes
```

Cela évite de déboguer 35 fois le même problème.

------------------------------------------------------------------------

# 15. Construire l'URL d'une ville

Selon le site / la page autorisée que tu utilises, tu peux soit :

### Méthode A --- construire directement l'URL

``` python
from urllib.parse import quote


def construire_url(city):
    city_encoded = quote(city)

    return f"URL_DE_RECHERCHE?destination={city_encoded}"
```

### Méthode B --- utiliser la barre de recherche

Playwright peut également reproduire les actions de l'utilisateur :

``` python
search = page.get_by_placeholder("Destination")

search.fill(city)

page.get_by_role("button", name="Rechercher").click()
```

Pour ton projet, **si une URL de recherche simple et stable existe, la
méthode A est plus simple**.

------------------------------------------------------------------------

# 16. Convertir les résultats en DataFrame

Une fois la liste remplie :

``` python
import pandas as pd


df_hotels = pd.DataFrame(all_hotels)
```

Affiche-la :

``` python
print(df_hotels.head())
```

Et vérifie :

``` python
print(df_hotels.shape)
print(df_hotels.columns)
```

------------------------------------------------------------------------

# 17. Nettoyage minimal

Ne fais pas un gros pipeline de nettoyage maintenant.

Quelques opérations simples suffisent.

### Supprimer les doublons

``` python
df_hotels = df_hotels.drop_duplicates()
```

### Supprimer les hôtels sans nom

``` python
df_hotels = df_hotels.dropna(subset=["name"])
```

### Réinitialiser l'index

``` python
df_hotels = df_hotels.reset_index(drop=True)
```

Tu pourras nettoyer précisément les prix et les notes plus tard.

------------------------------------------------------------------------

# 18. Exporter le CSV

``` python
df_hotels.to_csv(
    "hotels.csv",
    index=False,
    encoding="utf-8"
)
```

Tu obtiens :

``` text
hotels.csv
```

C'est ce fichier que tu pourras ensuite concaténer / joindre à tes
données de villes et de météo.

------------------------------------------------------------------------

# 19. Squelette complet minimal

Voici la structure générale à atteindre. **Les sélecteurs sont
volontairement à identifier sur la page que tu es autorisé à utiliser**,
car ils dépendent du HTML réel et peuvent changer.

``` python
from urllib.parse import quote

import pandas as pd
from playwright.sync_api import sync_playwright


CITIES = [
    "Paris",
    "Lyon",
    "Bordeaux",
]


def construire_url(city):
    city_encoded = quote(city)

    return f"URL_DE_RECHERCHE?destination={city_encoded}"


def get_text(card, selector):
    element = card.locator(selector)

    if element.count() == 0:
        return None

    return element.first.inner_text().strip()


all_hotels = []


with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)

    page = browser.new_page()

    for city in CITIES:

        print(f"Scraping : {city}")

        url = construire_url(city)

        page.goto(
            url,
            wait_until="domcontentloaded",
            timeout=60000
        )

        hotel_cards = page.locator(
            "SELECTEUR_CARTE_HOTEL"
        )

        hotel_cards.first.wait_for(
            state="visible",
            timeout=30000
        )

        print(
            "Hôtels trouvés :",
            hotel_cards.count()
        )

        for i in range(hotel_cards.count()):

            card = hotel_cards.nth(i)

            hotel = {
                "city": city,
                "name": get_text(
                    card,
                    "SELECTEUR_NOM"
                ),
                "price": get_text(
                    card,
                    "SELECTEUR_PRIX"
                ),
                "score": get_text(
                    card,
                    "SELECTEUR_NOTE"
                ),
            }

            all_hotels.append(hotel)

    browser.close()


df_hotels = pd.DataFrame(all_hotels)

df_hotels = df_hotels.drop_duplicates()

df_hotels = df_hotels.dropna(
    subset=["name"]
)

df_hotels = df_hotels.reset_index(
    drop=True
)

df_hotels.to_csv(
    "hotels.csv",
    index=False,
    encoding="utf-8"
)

print(df_hotels.head())

print(
    f"{len(df_hotels)} hôtels enregistrés."
)
```

------------------------------------------------------------------------

# 20. Si aucun hôtel n'est trouvé

Avant de modifier tout ton code, vérifie dans cet ordre.

### A. Voir ce que le navigateur affiche

Garde :

``` python
headless=False
```

Observe simplement la fenêtre.

Si la page visible n'est pas celle attendue, le problème n'est pas ton
sélecteur.

### B. Vérifier le titre et l'URL

``` python
print(page.title())
print(page.url)
```

### C. Sauvegarder une capture d'écran

``` python
page.screenshot(
    path="debug.png",
    full_page=True
)
```

Regarde `debug.png`.

### D. Sauvegarder le HTML rendu

``` python
html = page.content()

with open(
    "debug.html",
    "w",
    encoding="utf-8"
) as f:
    f.write(html)
```

Tu peux alors inspecter exactement ce que Playwright a reçu/rendu.

### E. Tester le locator

``` python
print(
    page.locator(
        "TON_SELECTEUR"
    ).count()
)
```

Si le résultat est :

``` text
0
```

ton sélecteur ne correspond à rien dans le DOM actuel.

------------------------------------------------------------------------

# 21. Si une bannière cookies gêne

Dans un cadre autorisé, traite-la comme un utilisateur normal : repère
le bouton et clique dessus.

Exemple générique :

``` python
button = page.get_by_role(
    "button",
    name="Accepter"
)

if button.count() > 0:
    button.first.click()
```

Ne cherche pas à contourner un CAPTCHA ou un système de blocage
automatisé. Si le site te bloque, arrête le scraping et vois avec
l'école quelle source ou autorisation utiliser.

------------------------------------------------------------------------

# 22. Faut-il utiliser BeautifulSoup en plus ?

Pour cette version : **non**.

Playwright sait déjà faire :

``` python
card.locator(...)
```

et :

``` python
element.inner_text()
```

Ajouter BeautifulSoup maintenant créerait une étape supplémentaire sans
nécessité.

Tu pourrais plus tard faire :

``` python
html = page.content()
```

puis analyser ce HTML avec BeautifulSoup, mais ce n'est pas nécessaire
pour atteindre ton objectif.

------------------------------------------------------------------------

# 23. Ce que tu dois faire concrètement

Travaille dans cet ordre :

``` text
ÉTAPE 1
Installer Playwright
        ↓
ÉTAPE 2
Ouvrir une page avec Chromium
        ↓
ÉTAPE 3
Ouvrir UNE page de résultats
        ↓
ÉTAPE 4
Trouver le locator d’une carte d’hôtel
        ↓
ÉTAPE 5
Afficher le texte de la première carte
        ↓
ÉTAPE 6
Trouver nom / prix / note
        ↓
ÉTAPE 7
Boucler sur tous les hôtels de cette ville
        ↓
ÉTAPE 8
Créer le DataFrame
        ↓
ÉTAPE 9
Exporter hotels.csv
        ↓
ÉTAPE 10
Tester avec 3 villes
        ↓
ÉTAPE 11
Passer aux 35 villes
```

**Ne passe à l'étape suivante que lorsque la précédente fonctionne.**

------------------------------------------------------------------------

# 24. Résultat final attendu

À la fin de cette partie, tu dois simplement avoir :

``` text
hotels.csv
```

avec par exemple :

``` text
city,name,price,score
Paris,Hotel A,120 €,8.4
Paris,Hotel B,98 €,7.9
Lyon,Hotel C,105 €,8.7
```

Ensuite seulement, tu pourras faire ta jointure avec ton DataFrame
contenant :

``` text
ville
latitude
longitude
météo
...
```

Typiquement :

``` python
df_final = df_hotels.merge(
    df_weather,
    on="city",
    how="left"
)
```

------------------------------------------------------------------------

## Références utiles

-   Documentation officielle Playwright Python --- Installation :
    https://playwright.dev/python/docs/intro
-   Documentation officielle --- Locators :
    https://playwright.dev/python/docs/locators
-   Documentation officielle --- Pages :
    https://playwright.dev/python/docs/pages
-   Conditions Booking.com :
    https://www.booking.com/content/terms.fr.html
