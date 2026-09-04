from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup

url = 'https://www.ambitionbox.com/list-of-companies'

with sync_playwright() as p: # sync_playwright() it means start the synchronous context manager
    browser = p.chromium.launch(headless=False)

    page = browser.new_page()

    page.goto(url)
    html = page.content()
    #print("Title:", page.title())
    #print("URL:", page.url)

    #text = page.locator("body").inner_text()
    soup = BeautifulSoup(html, 'lxml')
    #print(soup.find_all('h1')[0].text)
    #print(soup.find_all('h2'))
    companies = soup.find_all("h2",class_="companyCardWrapper__companyName") #class_="companyCardWrapper__companyName")

    for company in companies:
        print(company.text.strip())

    ratings = soup.find_all(class_='rating_text')

    for rating in ratings:
        print(rating.text.strip())

    company_rating_count = soup.find_all(x)
    for company_rating in company_rating_count:
        print(company_rating.text.strip())

    together = soup.find_all(class_="companyCardWrapper__interLinking")
    print(together)
    for item in together:
        text = item.get_text(" ", 1)
        industry,location = text.split('|', 1)
        industry = industry.strip()
        location = location.strip()

        city = location.split("+")[0].strip()
        other_location = location.split("+")[1].strip()
        print("Industry:", industry)
        print("City:", city)
        print("Other:", other_location)

    #print(soup)
    #print(text)
    browser.close()