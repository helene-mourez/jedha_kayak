import scrapy
from pathlib import Path
import logging
from scrapy.crawler import CrawlerProcess

class RandomQuoteSpider(scrapy.Spider):
    # Name of your spider
    name = "mySpider"

    # Url to start your spider from
    start_urls = [
        'https://www.booking.com/searchresults.fr.html?label=msn-8aGmFKcvjur7ORXD1T41Jg-80676853483926%3Atikwd-80677028168879%3Aloc-66%3Anes%3Amte%3Alp186792%3Adec%3Acid518941944%3Aagid1290827950458860%3Aclkida60dbefb136f17da04a9d47302b61cd6&aid=2369666&ss=Valensole%2C+Provence-Alpes-C%C3%B4te+d%27Azur+%28Plateau+de+Valensole%29%2C+France&efdco=1&lang=fr&src=index&dest_id=-1474456&dest_type=city&ac_position=0&ac_click_type=b&ac_langcode=fr&ac_suggestion_list_length=5&search_selected=true&search_pageview_id=43f73e73bcac020e&checkin=2026-08-24&checkout=2026-08-30&group_adults=1&no_rooms=1&group_children=0&nflt=ht_id%3D204'
        ]

    # Callback function that will be called when starting your spider
    def parse(self, response):
        self.logger.info("Page reçue : %s", response.url)
        self.logger.info("Statut HTTP : %s", response.status)
        self.logger.info(response.text[:500]) # méthode parse pour response.text[:500] et voir page de blocage AWS WAF protection antibot

        yield {
            "url": response.url,
            "status": response.status,
            "title": response.css("title::text").get(),
        }


output_dir = Path("data")
output_dir.mkdir(parents=True, exist_ok=True)
output_path = output_dir / "booking_scrap.json"

if output_path.exists():
    output_path.unlink()

# crawlerProcess
process = CrawlerProcess(
    settings={
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:154.0)",
        "LOG_LEVEL": logging.INFO,
        "DOWNLOAD_DELAY": 2,
        "FEEDS": {
            str(output_path): {
                "format": "json",
                "encoding": "utf-8",
                "indent": 2,
            },
        },
    }
)

process.crawl(RandomQuoteSpider)
process.start()

print(f"Résultat enregistré dans : {output_path.resolve()}")
