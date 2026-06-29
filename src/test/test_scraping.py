from scraper.scraper import  WebScraper, BBVAScraperStrategy

if __name__ == "__main__":
    urls_to_scrape = [        
        "https://www.davibank.com/",
        "https://www.davibank.com/personas/tarjeta-de-credito/tarjetas-one",
        "https://www.davibank.com/personas/tarjeta-de-credito/lifemiles",
        "https://www.davibank.com/personas/tarjeta-de-credito/especializadas/cencosud",
        "https://www.davibank.com/personas/tarjeta-de-credito/terpel",
        "https://www.davibank.com/personas/tarjeta-de-credito/especializadas/pricesmart"
    ]

    # Instanciamos el contexto pasándole la estrategia concreta
    scraper = WebScraper(strategy=BBVAScraperStrategy())
    scraper.execute_and_save(urls_to_scrape)