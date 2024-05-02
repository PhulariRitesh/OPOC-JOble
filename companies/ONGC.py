
import asyncio
import json
from playwright.async_api import async_playwright

async def scrape_ongc_jobs(page_number):
    async with async_playwright() as p:
        browser = await p.chromium.launch(ignoreHTTPSErrors=True)  # Corrected parameter name
        page = await browser.new_page()

        await page.goto(f"https://ongcindia.com/web/eng/search?q=job&delta=20&start={page_number}")

        # Wait for job listings to load
        await page.wait_for_load_state("networkidle")

        # Extract job listings
        job_listings = await page.evaluate('''() => {
            const listings = []
            document.querySelectorAll('.list-group-item').forEach(job => {
                const titleElement = job.querySelector('.list-group-title');
                const dateElement = job.querySelector('.list-group-subtitle');
                const descriptionElement = job.querySelector('.subtext-item');
                const linkElement = job.querySelector('a');

                if (titleElement && dateElement && descriptionElement && linkElement) {
                    const title = titleElement.innerText.trim();
                    const date = dateElement.innerText.trim();
                    const description = descriptionElement.innerText.trim();
                    const link_ex = linkElement.getAttribute('href');
                    const link = `ongcindia.com${link_ex}`
                    listings.push({
                        title,
                        date,
                        description,
                        link
                    });
                }
            });
            return listings;
        }''')

        return job_listings


async def save_job_listings_to_json():
    all_jobs = []
    for i in range(20, 40):  # Accessing pages from 1 to 39
        jobs_on_page = await scrape_ongc_jobs(i)
        all_jobs.extend(jobs_on_page)

    with open('ongc_job_2.json', 'w') as f:
        json.dump(all_jobs, f, indent=4)

asyncio.run(save_job_listings_to_json())
