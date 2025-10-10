# Main file to call all modules

scraper = Scraper()

scraped_data = scraper.scrap()

translator = Translator()

data = translator.translate(scraped_data)