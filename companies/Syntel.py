import requests
from bs4 import BeautifulSoup
import json

def scrape_syntel_telecom_jobs():
    url = "https://synteltelecom.com/careers/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the table element
    table = soup.find('table', class_='table')

    job_listings = []

    # Extract data from table rows
    for row in table.find_all('tr')[1:]:  # Skip the header row
        columns = row.find_all('td')
        job = {
            "Sr. #": columns[0].text.strip(),
            "Position": columns[1].text.strip(),
            "Role": columns[2].text.strip(),
            "Product Portfolio": columns[3].text.strip(),
            "Division": columns[4].text.strip(),
            "Years of Exp": columns[5].text.strip(),
            "Location": columns[6].text.strip(),
        }
        job_listings.append(job)

    return job_listings

def save_job_listings_to_json(job_listings):
    with open('syntel_telecom_jobs.json', 'w') as f:
        json.dump(job_listings, f, indent=4)

if __name__ == "__main__":
    job_listings = scrape_syntel_telecom_jobs()
    save_job_listings_to_json(job_listings)
