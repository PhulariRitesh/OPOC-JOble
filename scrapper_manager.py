from apscheduler.schedulers.blocking import BlockingScheduler
from scrapper_base import Scrapper
from typing import List
from logger import logger


class ScrapperManager:
    def __init__(self):
        self.scrappers: List[Scrapper] = []
        self.scheduler = BlockingScheduler()

    def register_scrapper(self, scrapper: Scrapper):
        self.scrappers.append(scrapper)

    def start(self):
        logger.info("Scheduler started")
        for scrapper in self.scrappers:
            self.scheduler.add_job(scrapper.scrape, 'interval', days=1)
        try:
            self.scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            logger.info("Scheduler stopped")
            self.scheduler.shutdown()
            logger.info("Scheduler shutdown")
            exit(0)
