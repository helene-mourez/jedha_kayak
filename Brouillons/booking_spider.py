import logging
from pathlib import Path

import scrapy
from scrapy.crawler import CrawlerProcess


class BookingSpider(scrapy.Spider):
    name = "booking"

    start_urls = [
        "https://www.booking.com/searchresults.fr.html?ss=Saint-Malo&ssne=Saint-Malo&ssne_untouched=Saint-Malo&label=gog235jc-10CAEoggI46AdIDVgDaE2IAQGYATO4AQfIAQ3YAQPoAQH4AQGIAgGoAgG4Ar-loNQGwAIB0gIkYjYzZjhkNmMtNzY3MS00ZDZlLWFlYmUtNjU4MWFhMTlkNTE12AIB4AIB&sid=08121f1474c0cb46b3ca9b8928a700ef&aid=397594&lang=fr&sb=1&src_elem=sb&src=index&dest_id=-1466824&dest_type=city&checkin=2026-08-21&checkout=2026-08-22&group_adults=2&no_rooms=1&group_children=0"
    ]

    def parse(self, response):
        self.logger.info("Page reçue : %s", response.url)
        self.logger.info("Statut HTTP : %s", response.status)
        self.logger.info(
            "Titre : %s",
            response.xpath("normalize-space(//title)").get(default="Titre absent"),
        )
        self.logger.info(
            "Extrait HTML : %s",
            " ".join(response.xpath("//body//text()").getall())[:500],
        )

        response.save("data/booking_debug.html")

        cards = response.xpath('//div[@data-testid="property-card"]')
        self.logger.info("Nombre de cartes trouvées : %d", len(cards))

        for card in cards:
            relative_url = card.xpath(
                './/a[@data-testid="title-link"]/@href'
            ).get()

            yield {
                "name": card.xpath(
                    'normalize-space(.//div[@data-testid="title"])'
                ).get(default=""),

                "address": card.xpath(
                    'normalize-space(.//span[@data-testid="address"])'
                ).get(default=""),

                "price": card.xpath(
                    'normalize-space(.//span[@data-testid="price-and-discounted-price"])'
                ).get(default=""),

                "review_score": card.xpath(
                    'normalize-space(.//div[@data-testid="review-score"])'
                ).get(default=""),

                "url": response.urljoin(relative_url) if relative_url else None,
            }


output_dir = Path("data")
output_dir.mkdir(parents=True, exist_ok=True)
output_path = output_dir / "booking_scrap.json"

if output_path.exists():
    output_path.unlink()

process = CrawlerProcess(
    settings={
        "USER_AGENT": "Mozilla/5.0",
        "LOG_LEVEL": logging.INFO,
        "FEEDS": {
            str(output_path): {
                "format": "json",
                "encoding": "utf-8",
                "indent": 2,
            },
        },
    }
)

process.crawl(BookingSpider)
process.start()

print(f"Résultat enregistré dans : {output_path.resolve()}")