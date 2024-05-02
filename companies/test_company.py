from scrapper_base import Scrapper, sample_data
from fake_data import generate_sample_data
# your function that scrapes the data from the website


def my_scrapper_function():
    return [generate_sample_data(), generate_sample_data(), generate_sample_data()]


# create a scrapper object by passing the scrapper function
scrapper = Scrapper(my_scrapper_function)
