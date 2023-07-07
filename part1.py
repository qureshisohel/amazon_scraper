import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_product_listing(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    products = soup.find_all('div', {'data-component-type': 's-search-result'})

    data = []
    for product in products:
        product_url = 'https://www.amazon.in' + product.find('a', {'class': 'a-link-normal s-no-outline'})['href']
        product_name = product.find('span', {'class': 'a-size-medium a-color-base a-text-normal'}).text.strip()
        product_price = product.find('span', {'class': 'a-price-whole'}).text.strip()

        rating_element = product.find('span', {'class': 'a-icon-alt'})
        rating = rating_element.text.strip() if rating_element else ''

        reviews_element = product.find('span', {'class': 'a-size-base'})
        reviews = reviews_element.text.strip() if reviews_element else ''

        data.append([product_url, product_name, product_price, rating, reviews])

    return data

# Scrape product listing pages
base_url = 'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_'
num_pages = 20

all_data = []
for page in range(1, num_pages + 1):
    url = base_url + str(page)
    page_data = scrape_product_listing(url)
    all_data.extend(page_data)

# Export data to CSV
df = pd.DataFrame(all_data, columns=['Product URL', 'Product Name', 'Product Price', 'Rating', 'Number of Reviews'])
df.to_csv('amazon_product_listing.csv', index=False)
