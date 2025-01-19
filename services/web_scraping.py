import requests
from bs4 import BeautifulSoup
import pandas as pd
from sqlalchemy import table

# Define the prompt and source
prompt = "Extract the title, price and availability of all books on this page."
source = "http://books.toscrape.com/"
source =  "https://carsheet.io/aston-martin,audi,bentley,bmw,ferrari,ford,mercedes-benz/2024/2-door/"
last_page = 100

# Create the scraper graph
def scrape(url):
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup

# find all relevant elements on the page
def scrape_page(soup, data):
    try:
        # ele_list = soup.find_all("div", class_="car-item")   #   product_pod")
        # find table
        html_elements = soup.find("table", {'id': 'carsheet'})
        if html_elements is None:
            print("Table not found")
            return

        # Extract headers
        table_headers = [th.text.strip() for th in html_elements.find_all("th")]
        # print(headers)

        # find all tr in table
        rows = html_elements.find_all("tr")[1:]
    
        for row in rows:
            cols = row.find_all("td")
            if len(cols) == len(table_headers):
                car_info = {table_headers[i]: cols[i].text.strip() for i in range(len(table_headers))}                                
                data.append(car_info)
    except requests.RequestException as e:
        print(f"Error: {e}")

def scrape_all_pages(soup, data):
    # for several pages in range
    page_range = [f"{i}-{i+50}" for i in range(0, last_page, 50)] 

    for page in page_range:
        url = f"{source}{page}"
        scrape_page(scrape(url), data)

# Scrapping
data = []   
scrape_all_pages(scrape(source), data)
df = pd.DataFrame(data)
df = df.drop_duplicates()
df.to_csv("cars_data.csv", index=False)



