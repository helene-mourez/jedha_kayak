from playwright.sync_api import sync_playwright
import time # temporisation
import random
from bs4 import BeautifulSoup

url = "https://www.booking.com/searchresults.fr.html?ss=Valensole&ssne=Valensole&ssne_untouched=Valensole&efdco=1&label=msn-8aGmFKcvjur7ORXD1T41Jg-80676853483926%3Atikwd-80677028168879%3Aloc-66%3Anes%3Amte%3Alp186792%3Adec%3Acid518941944%3Aagid1290827950458860%3Aclkida60dbefb136f17da04a9d47302b61cd6&aid=2369666&lang=fr&sb=1&src_elem=sb&src=searchresults&dest_id=-1474456&dest_type=city&checkin=2026-08-21&checkout=2026-08-22&group_adults=2&no_rooms=1&group_children=0"

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
    print(html[:500])
    browser.close()

    '''page.query_selector_all(...) (Playwright) interroge directement le navigateur ouvert en mémoire — pratique si tu veux interagir avec la page (cliquer, scroller) en même temps que tu extrais des données, mais un peu plus lent et dépend que le navigateur reste ouvert. BeautifulSoup parse le HTML une fois récupéré (page.content()), en dehors du navigateur — plus rapide pour extraire beaucoup de données, syntaxe plus simple avec .find()/.find_all(), et tu peux fermer le navigateur juste après avoir récupéré le HTML. Pour ton cas (scraper 50 villes, juste extraire du texte sans interagir avec la page), BeautifulSoup est recommandé : plus simple à un niveau scolaire, et tu libères le navigateur plus vite. Veux-tu qu'on parte sur BeautifulSoup pour extraire les données des hôtels ?
    
    page.query_selector_all(...) (Playwright) interroge directement le navigateur ouvert en mémoire — pratique si tu veux interagir avec la page (cliquer, scroller) en même temps que tu extrais des données, mais un peu plus lent et dépend que le navigateur reste ouvert. BeautifulSoup parse le HTML une fois récupéré (page.content()), en dehors du navigateur — plus rapide pour extraire beaucoup de données, syntaxe plus simple avec .find()/.find_all(), et tu peux fermer le navigateur juste après avoir récupéré le HTML. Pour ton cas (scraper 50 villes, juste extraire du texte sans interagir avec la page), BeautifulSoup est recommandé : plus simple à un niveau scolaire, et tu libères le navigateur plus vite. Veux-tu qu'on parte sur BeautifulSoup pour extraire les données des hôtels ?
    
    Pour la suite, il faut identifier les sélecteurs des hôtels : ouvre le lien de ton url directement dans Chrome, attends que la page de résultats hôtels s'affiche complètement, puis fais clic droit sur le nom d'un hôtel visible → Inspecter. Dis-moi le nom de la balise (div, span, a...) et sa classe ou son attribut data-testid affichés dans l'inspecteur à cet endroit précis.
    
    Changer d'IP n'est pas indispensable à ce stade : ton script fonctionne déjà (tu as récupéré la vraie page HTML), donc le blocage initial était lié au rendu JavaScript, pas à ton IP. Le risque de bannissement IP existe surtout si tu fais beaucoup de requêtes rapprochées (ex: 50 villes sans pause), ce que tu évites déjà avec ta tempo aléatoire de 3-6 secondes. Une seule requête ponctuelle comme celle-ci ne devrait pas suffire à bannir ton IP. Si tu scrapes les 50 villes plus tard et rencontres un nouveau blocage, on pourra alors envisager un VPN ou un service de proxy rotatif. Le document projet ne mentionne pas cette exigence, donc ce n'est pas une obligation du projet.
    
    Parfait, soup.title confirme que BeautifulSoup fonctionne bien et lit la vraie page Booking.com (titre "Hôtels : Valensole"). Maintenant il nous faut identifier les sélecteurs CSS des hôtels eux-mêmes. Ouvre l'url dans Chrome, attends le chargement complet des résultats, puis fais un clic droit sur le nom d'un hôtel dans la liste → Inspecter. Dis-moi la balise et la classe/attribut qui apparaissent en surbrillance dans l'inspecteur (par exemple quelque chose comme <div data-testid="title">Nom de l'hôtel</div>).
    '''