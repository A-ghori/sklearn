from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pandas as pd
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False, args=["--disable-http2"])
    page = browser.new_page(
        user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
    )

    all_data = []
    page_number = 1
    failed_pages = []

    while True:

        # Har page ke liye success reset
        success = False

        url = 'https://www.ambitionbox.com/list-of-companies?pages={}'.format(page_number)

        for attempt in range(1, 4):
            try:
                print(f"Scraping page {page_number}...")

                page.goto(
                    url,
                    wait_until="domcontentloaded",
                    timeout=60000
                )

                html = page.content()
                soup = BeautifulSoup(html, 'lxml')

                print(f"Pages {page_number} completed")

                success = True
                break

            except Exception as e:
                print(f"Page {page_number} failed: {e}")

                if attempt < 3:
                    time.sleep(3)

        if not success:
            print(
                f"Page {page_number} failed "
                f"after 3 attempts"
            )

            failed_pages.append(page_number)

            page_number += 1
            continue

        company_name = []
        rating = []
        reviews = []
        industry = []
        city = []
        location_others = []
        salaries = []
        interviews = []
        jobs = []
        photos = []
        benifits = []

        together = soup.find_all(
            class_="companyCardWrapper__interLinking"
        )

        for item in together:

            text = item.get_text(' ', 1)
            industry_name, location = text.split('|', 1)

            industry.append(
                industry_name.strip()
            )

            location = location.strip()

            city.append(
                location.split("+")[0].strip()
            )

            location_others.append(
                location.split("+")[1].strip()
            )

        company = soup.find_all(
            'div',
            class_="companyCardWrapper__primaryInformation"
        )

        for i in company:

            company_name.append(
                i.find(
                    'h2',
                    class_="companyCardWrapper__companyName"
                ).text.strip()
            )

            rating.append(
                i.find(
                    class_='rating_text'
                ).text.strip()
            )

            reviews.append(
                i.find(
                    class_="companyCardWrapper__companyRatingCount"
                ).text.strip().strip("()")
            )

        company_footer = soup.find_all(
            'div',
            class_='companyCardWrapper__tertiaryInformation'
        )

        for i in company_footer:

            salaries.append(
                i.find_all(
                    'span',
                    class_="companyCardWrapper__ActionCount"
                )[1].text.strip()
            )

            interviews.append(
                i.find_all(
                    'span',
                    class_="companyCardWrapper__ActionCount"
                )[2].text.strip()
            )

            jobs.append(
                i.find_all(
                    'span',
                    class_="companyCardWrapper__ActionCount"
                )[3].text.strip()
            )

            benifits.append(
                i.find_all(
                    'span',
                    class_="companyCardWrapper__ActionCount"
                )[4].text.strip()
            )

            photos.append(
                i.find_all(
                    'span',
                    class_="companyCardWrapper__ActionCount"
                )[5].text.strip()
            )

        # Creating Dataframe
        d = {
            'company_name': company_name,
            'rating': rating,
            'reviews': reviews,
            'industry': industry,
            'location_others': location_others,
            'city': city,
            'salaries': salaries,
            'interviews': interviews,
            'jobs': jobs,
            'benifits': benifits,
            'photos': photos
        }

        # Current page ka data add karo
        all_data.extend(
            pd.DataFrame(d).to_dict('records')
        )

        # Total dataframe
        df = pd.DataFrame(all_data)

        print(
            f"✅ Page {page_number} completed | "
            f"{len(df)} total companies"
        )

        # Checkpoint save
        if page_number % 20 == 0:

            df.to_csv(
                "ambitionbox_companies.csv",
                index=False
            )

            print(
                f"Checkpoint saved after page {page_number}"
            )

        print(df.shape)

        page_number += 1