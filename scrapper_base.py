from typing import List, Dict, Callable
from logger import logger
from pymongo import MongoClient
import os

sample_data = {
    "title": "Software Engineer",
    "company": "Google",
    "experience": "2 years",
    "description": "The job description",
    "job_link": "https://www.google.com",
    "location": "Mountain View, CA",
    "date": "2021-01-01",
    "salary": "100000 - 150000 USD",
    "company_link": "https://www.google.com",
    "education": "Bachelor's degree",
    "employment_type": "Full-time",
    "role": "Software Engineer",
    "skills": ["python", "java", "c++"],
    "jobid": "12345",
    # Add more fields as needed
}
REQUIRED_KEYS = set(sample_data.keys())

mongo_uri = os.getenv("MONGO_URI")
if not mongo_uri:
    logger.error("MONGO_URI not set. Exiting")
    exit(1)
client = MongoClient(mongo_uri)


class JobData:
    def __init__(self, data: List[Dict]):
        self.data = data
        self.db = client["jobs"]
        self.collection = self.db["jobs_data"]

    def verify_data(self):
        logger.info("Verifying the data")
        for job in self.data:
            assert REQUIRED_KEYS.issubset(
                set(job.keys())), "Invalid keys in the data"

        logger.info("Data verified successfully")
        return self.data

    def save_data(self):
        logger.info(f"Saving {len(self.data)} jobs to the database")
        self.collection.insert_many(self.data)
        logger.info("Data saved successfully")

    def clear_data(self):
        logger.info("Clearing the database")
        self.collection.delete_many({})
        logger.info("Database cleared")


class Scrapper:
    def __init__(self, scrapper_func: Callable[..., List[Dict]]):
        self.scrapper_func = scrapper_func

    def scrape(self, verify_data: bool = True, save_data: bool = True):
        data = self.scrapper_func()
        job_data = JobData(data)
        if verify_data:
            job_data.verify_data()
        if save_data:
            job_data.save_data()

        logger.info(
            f"Scrapped {len(data)} jobs - for {job_data.data[0]['company']}")
        return data


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
    client = MongoClient(mongo_uri)
    # cli
    todo = int(input("What do you want to do? [scrape(0)/clear(1)]: "))
    if todo == 0:
        # your function that scrapes the data from the website
        from fake_data import generate_sample_data

        def my_scrapper_function():
            return [generate_sample_data(), generate_sample_data(), generate_sample_data()]

        scrapper = Scrapper(my_scrapper_function)
        scrapper.scrape()
    elif todo == 1:
        job_data = JobData([])
        job_data.clear_data()
    else:
        print("Invalid input")
