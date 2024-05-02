from dotenv import load_dotenv
load_dotenv()
from logger import logger
from scrapper_manager import ScrapperManager
from companies.test_company import scrapper as TestCompanyScrapper

logger.info("Starting the scrapper manager")
scrapper_manager = ScrapperManager()

# Register scrappers here, add more below as needed
scrapper_manager.register_scrapper(TestCompanyScrapper)


# Start the scheduler
scrapper_manager.start()
