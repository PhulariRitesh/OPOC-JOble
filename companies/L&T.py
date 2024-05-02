import asyncio
import json
from playwright.async_api import async_playwright

async def scrape_larsen_tourbo_jobs():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        await page.goto("https://larsentoubrocareers.peoplestrong.com/job/joblist")

        # Wait for job listings to load
        await page.wait_for_load_state("networkidle")

        # Extract job listings
        job_listings = await page.evaluate('''() => {
            const listings = []
            document.querySelectorAll('.card-block-inner').forEach(job => {
                const titleElem = job.querySelector('.title_block a');
                const job_codeElem = job.querySelector('.job-code');
                const business_unitElem = job.querySelector('.orgunit-row li:first-child');
                const locationElem = job.querySelector('.orgunit-row li:nth-child(2)');
                const posted_dateElem = job.querySelector('.last-child .link2');
                const experienceElem = job.querySelector('.card-row:nth-child(3) .font-bold');
                const required_skillsElems = job.querySelectorAll('.required-experience-row .skill-row .tag-job');

                // Check if elements exist before accessing their properties
                if (titleElem && job_codeElem && business_unitElem && locationElem && posted_dateElem && experienceElem) {
                    const title = titleElem.innerText.trim();
                    const job_code = job_codeElem.innerText.trim();
                    const business_unit = business_unitElem.innerText.trim();
                    const location = locationElem.innerText.trim();
                    const posted_date = posted_dateElem.innerText.trim();
                    const experience = experienceElem.innerText.trim();
                    const required_skills = Array.from(required_skillsElems).map(skill => skill.innerText.trim());
                    
                    listings.push({
                        title,
                        job_code,
                        business_unit,
                        location,
                        posted_date,
                        experience,
                        required_skills
                    });
                }
            });
            return listings;
        }''')

        return job_listings

async def save_job_listings_to_json():
    try:
        jobs = await scrape_larsen_tourbo_jobs()
        with open('larsen_tourbo_jobs.json', 'w') as f:
            json.dump(jobs, f, indent=4)
    except Exception as e:
        print(f"An error occurred: {e}")

asyncio.run(save_job_listings_to_json())
