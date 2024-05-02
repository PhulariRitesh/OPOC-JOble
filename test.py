from dotenv import load_dotenv
load_dotenv()
import unittest
from scrapper_manager import ScrapperManager
from scrapper_base import sample_data
from companies.test_company import scrapper as TestCompanyScrapper

class TestScrappers(unittest.TestCase):
    def setUp(self):
        self.scrapper_manager = ScrapperManager()
        self.scrapper_manager.register_scrapper(TestCompanyScrapper)

    def test_scrappers(self):
        for scrapper in self.scrapper_manager.scrappers:
            data = scrapper.scrape(verify_data=True, save_data=False)
            print(data)
            # Check that the data is a list
            # self.assertIsInstance(data, list)
            # Check that each item in the list is a dictionary
            # for item in data:
            #     self.assertIsInstance(item, dict)


if __name__ == '__main__':
    unittest.main()
