import csv
import requests
from bs4 import BeautifulSoup

def scrape_page(soup, quotes):
    # Retrieve all 'div' elements
    quote_elements = soup.find_all('div', class_='quote')

    for quote_element in quote_elements:
        text = quote_element.find('span', class_='text').text

        author = quote_element.find('small', class_= 'author').text

        # extract tag ele
        tag_elements = quote_element.find('div', class_='tags').find_all('a', class_='tag')

        tags = []
        for tag_element in tag_elements:
            tags.append(tag_element.text)

        quotes.append(
            {
                'text': text,
                'author': author,
                'tags': ', '.join(tags)
            }
        )


base_url = 'https://quotes.toscrape.com'

# defining the User-Agent header to use in the GET request below
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
}

# retrieve target web pages
page = requests.get(base_url, headers=headers)

# parse the page
soup = BeautifulSoup(page.text, 'html.parser')

# collect quotes
quotes = []

# scrape
scrape_page(soup, quotes)

next_li_element = soup.find('li', class_='next')

while next_li_element is not None:
    next_page_rel_url = next_li_element.find('a', href=True)['href']

    page = requests.get(base_url + next_page_rel_url, headers=headers)

    soup = BeautifulSoup(page.text, 'html.parser')

    scrape_page(soup, quotes)

    next_li_element = soup.find('li', class_='next')

# write to a csv file
csv_file = open('quotes.csv', 'w', encoding='utf-8', newline='')

writer = csv.writer(csv_file)

# write csv header
writer.writerow(['Text', 'Author', 'Tags'])

# write each row
for quote in quotes:
    writer.writerow(quote.values())

csv_file.close()
