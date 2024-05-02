import asyncio
import json
from playwright.async_api import async_playwright

async def scrape_razorpay_jobs():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        job_listings = []

        for page_number in range(1, 10):  # Assuming there are 5 pages, adjust as needed
            url = f"https://razorpay.com/jobs/jobs-all/?location=all&department=&page={page_number}"
            await page.goto(url)

            # Wait for job listings to load
            await page.wait_for_load_state("networkidle")

            # Extract job listings on the current page
            listings_on_page = await page.evaluate('''() => {
                const listings = [];
                document.querySelectorAll('.styles_container__LrNWu').forEach(job => {
                    const title = job.querySelector('.styles_jobTitle__ZewFx')?.innerText?.trim() || '';
                    const department = job.querySelector('.styles_jobDept__cpd2J')?.innerText?.trim() || '';
                    const locationElement = job.querySelector('.styles_jobDept__cpd2J svg').parentNode; // Get the parent node of the SVG
                    const location_ex = locationElement.innerText.trim(); // Extract the text content of the parent node
                    const location_e = location_ex.split('/');
                    const location = location_e[0];
                    const jobDesignation = department.split('/').pop().trim();

                    const anchorElement = document.querySelector('.row.styles_container__LrNWu');

                    const link_ex = anchorElement.getAttribute('href');

                    const link = `razorpay.com${link_ex}`;


                    listings.push({
                        title,
                        jobDesignation,
                        location,
                        link
                    });
                });
                return listings;
            }''')

            job_listings.extend(listings_on_page)

        return job_listings

async def save_job_listings_to_json():
    jobs = await scrape_razorpay_jobs()
    with open('razorpay_job.json', 'w') as f:
        json.dump(jobs, f, indent=4)

asyncio.run(save_job_listings_to_json())
