import asyncio
import json
from playwright.async_api import async_playwright

async def scrape_microsoft_jobs(page_number):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        url = f"https://careers.microsoft.com/us/en/search-results?keywords=python&page={page_number}"
        await page.goto(url)

        try:
            # Wait for job listings to load
            await page.wait_for_load_state("networkidle", timeout=600000)  # Increase timeout to 60 seconds

            # Increase waiting time for job listings to appear
            await asyncio.sleep(5)

            # Extract job listings
            job_listings = await page.evaluate('''() => {
                const listings = []
                document.querySelectorAll('div.job-result').forEach(job => {
                    const title = job.querySelector('h2.job-title').innerText.trim();
                    const location = job.querySelector('span.job-location').innerText.trim();
                    const description = job.querySelector('div.job-description').innerText.trim();
                    
                    listings.push({
                        title,
                        location,
                        description
                    });
                });
                return listings;
            }''')

            return job_listings
        except asyncio.TimeoutError:
            print(f"Timeout error occurred while scraping page {page_number}")
            return []

async def scrape_microsoft_jobs_with_retry(page_number, max_retries=3):
    retries = 0
    while retries < max_retries:
        try:
            return await scrape_microsoft_jobs(page_number)
        except asyncio.TimeoutError:
            print(f"Timeout error occurred while scraping page {page_number}. Retrying ({retries + 1}/{max_retries})...")
            retries += 1
    print(f"Max retries ({max_retries}) reached for page {page_number}. Skipping...")
    return []

async def save_job_listings_to_json():
    all_jobs = []
    try:
        tasks = []
        for page_number in range(1, 6):  # Adjust the range as needed
            tasks.append(scrape_microsoft_jobs_with_retry(page_number))
        
        all_jobs = await asyncio.gather(*tasks)
    except Exception as e:
        print("An error occurred:", e)
    finally:
        with open('microsoft_jobs.json', 'w') as f:
            json.dump(all_jobs, f, indent=4)

asyncio.run(save_job_listings_to_json())
