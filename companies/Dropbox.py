async def scrape_dropbox_jobs():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        await page.goto("https://jobs.dropbox.com/all-jobs")

        # Wait for job listings to load
        await page.wait_for_load_state("networkidle")

        # Extract job listings
        job_listings = await page.evaluate('''() => {
            const listings = []
            document.querySelectorAll('.open-positions__listing').forEach(job => {
                const title = job.querySelector('.open-positions__listing-title').innerText.trim();
                let location = job.querySelector('.open-positions__listing-location').innerText.trim();
                const link = job.querySelector('.open-positions__listing-link').getAttribute('href');

                // Remove "Remote" from the location if it exists
                location = location.replace('Remote - ', '');

                listings.push({
                    title,
                    location,
                    link
                });
            });
            return listings;
        }''')

        return job_listings
