import asyncio
import json
from playwright.async_api import async_playwright

async def scrape_capgemini_jobs():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        await page.goto("https://www.capgemini.com/in-en/careers/job-search__trashed/?country_code=in-en&country_name=India&size=605")

        # Wait for job listings to load
        await page.wait_for_load_state("networkidle")

        # Extract job listings
        job_listings = await page.evaluate('''() => {
            const listings = []
            document.querySelectorAll('.table-tr.joblink').forEach(job => {
                const title = job.querySelector('.table-td-header').innerText.trim();
                const location = job.querySelector('.table-td:nth-child(3) div').innerText.trim();
                const experience_level = job.querySelector('.table-td:nth-child(4) div').innerText.trim();
                const professional_communities = job.querySelector('.table-td:nth-child(5) div').innerText.trim();
                const contract_type = job.querySelector('.table-td:nth-child(6) div').innerText.trim();
                const brand = job.querySelector('.table-td:nth-child(8) div').innerText.trim();
                
                // Additional information
                const job_name_element = job.querySelector('.table-td:nth-child(1) div');
                const [job_name, experience, city_name] = job_name_element.innerText.trim().split(' | ');
                const country = job.querySelector('.table-td:nth-child(2) div').innerText.trim();
                const business_unit = job.querySelector('.table-td:nth-child(7) div').innerText.trim();

                listings.push({
                    title,
                    location,
                    experience_level,
                    professional_communities,
                    contract_type,
                    brand,
                    job_name,
                    experience,
                    city_name,
                    country,
                    business_unit
                });
            });
            return listings;
        }''')

        return job_listings

async def save_job_listings_to_json():
    jobs = await scrape_capgemini_jobs()
    with open('capgemini_job.json', 'w') as f:
        json.dump(jobs, f, indent=4)

asyncio.run(save_job_listings_to_json())
