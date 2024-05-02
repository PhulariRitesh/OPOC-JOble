import requests
from bs4 import BeautifulSoup
import json

def scrape_trilogy_jobs():
    url = "https://www.crossover.com/clients/trilogy"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    jobs_data = []
    
    job_cards = soup.find_all(class_='jobcard-card-info')
    
    for card in job_cards:
        job_title = card.find(class_='title').text.strip()
        salary = card.find(class_='salary').text.strip()
        location = card.find(class_='chip-text').text.strip()
        hours = card.find(class_='hours').text.strip()
        job_type = card.find_all(class_='chip-text')[-1].text.strip()
        
        job_data = {
            'job_title': job_title,
            'salary': salary,
            'location': location,
            'hours': hours,
            'job_type': job_type
        }
        jobs_data.append(job_data)
    
    return jobs_data

def save_to_json(data, filename):
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)

if __name__ == "__main__":
    jobs = scrape_trilogy_jobs()
    save_to_json(jobs, 'trilogy_jobs.json')
