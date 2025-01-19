import csv
from mmap import PAGESIZE
import requests
from bs4 import BeautifulSoup

# Create the scraper graph
def scrape(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup

def scrape_page(soup, data):
    # retirieve all quote <div class="quote"> html elements
    html_elements = soup.find_all("div", class_="quote")

    for element in html_elements:
        # extract text from quote and author
        text = element.find("span", class_="text").text
        author = element.find("small", class_="author").text

        # extract tag <a> elements from quote
        tag_elements = element.find("div", class_="tags").find_all("a", class_="tag")

        tags = [tag.text for tag in tag_elements]

        data.append({
            "quote": text,
            "author": author,
            "tags": ', '.join(tags) if tags else None
        })

def scrape_all_pages(soup, data):
    # scrape first page
    scrape_page(soup, data)

    # scrape next pages
    next_page_link = soup.find("li", class_="next").find("a")
    while next_page_link:
        print(f"next page: {source}{next_page_link['href']}")
        url = f"{source}{next_page_link['href']}"
        soup = scrape(url)
        scrape_page(soup, data)
        next_link = soup.find("li", class_="next")
        if next_link:
            next_page_link = next_link.find("a")
        else:
            next_page_link = None
        # next_page_link = soup.find("li", class_="next").find("a") if soup.find("li", class_="next").find("a") else None

data = []
source = "http://quotes.toscrape.com/"
soup = scrape(source)
scrape_all_pages(soup, data)

# wrtite to csv file
with open("quotes.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["quote", "author", "tags"])
    writer.writerows(data)
