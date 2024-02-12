import requests
from bs4 import BeautifulSoup
import json

base_url = "http://quotes.toscrape.com"
quotes_url = "/page/1"
quotes_data = []

while quotes_url:

    response = requests.get(f"{base_url}{quotes_url}")
    soup = BeautifulSoup(response.text, 'html.parser')

    for quote in soup.find_all('div', class_='quote'):
        text = quote.find('span', class_='text').text
        author = quote.find('small', class_='author').text
        tags = [tag.text for tag in quote.find_all('a', class_='tag')]

        quotes_data.append({
            "text": text,
            "author": author,
            "tags": tags
        })

    next_page = soup.find('li', class_='next')
    quotes_url = next_page.find('a')['href'] if next_page else None

with open('quotes.json', 'w', encoding='utf-8') as quotes_file:
    json.dump(quotes_data, quotes_file, ensure_ascii=False, indent=2)

authors_data = [{"fullname": author["author"]} for author in quotes_data]
authors_data = list({author["fullname"]: author for author in authors_data}.values())

with open('authors.json', 'w', encoding='utf-8') as authors_file:
    json.dump(authors_data, authors_file, ensure_ascii=False, indent=2)

print("Scraping completed. JSON files saved.")
