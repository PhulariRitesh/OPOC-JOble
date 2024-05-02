import requests
from bs4 import BeautifulSoup
import json
import time

def scrape_jobs(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    job_items = []

    while url:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to retrieve page {url}")
            return job_items

        soup = BeautifulSoup(response.content, 'html.parser')
        
        for item in soup.find_all('div', class_='ms-List-cell'):
            job_data = {}
            title_elem = item.find('h2', class_='MZGzlrn8gfgSs8TZHhv2')
            job_data['title'] = title_elem.text.strip() if title_elem else 'N/A'
            posted_elem = item.find('i', {'data-icon-name': 'Clock'}).find_next_sibling()
            job_data['posted'] = posted_elem.text.strip() if posted_elem else 'N/A'
            location_elem = item.find('i', {'data-icon-name': 'POI'}).find_next_sibling()
            job_data['location'] = location_elem.text.strip() if location_elem else 'N/A'
            flexibility_elem = item.find('i', {'data-icon-name': 'AddHome'}).find_next_sibling()
            job_data['flexibility'] = flexibility_elem.text.strip() if flexibility_elem else 'N/A'
            description_elem = item.find('span', class_='css-539')
            job_data['description'] = description_elem.text.strip() if description_elem else 'N/A'
            job_items.append(job_data)
        
        next_page_elem = soup.find('a', class_='page-next')
        url = next_page_elem['href'] if next_page_elem else None
        time.sleep(1)  # Adding a delay to avoid hitting the server too frequently

    return job_items

def save_to_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

url = "https://jobs.careers.microsoft.com/global/en/search?l=en_us&pg=1&pgSz=20&o=Relevance"
jobs_data = scrape_jobs(url)
save_to_json(jobs_data, 'microsoft_jobs.json')
