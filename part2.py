import requests
from bs4 import BeautifulSoup
import csv

# Part 1: Scraping product data from the listing pages
def scrape_listing_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    products = []
    results = soup.find_all('div', {'data-component-type': 's-search-result'})
    
    for result in results:
        product = {}
        
        # Extracting product information
        link = result.find('a', {'class': 'a-link-normal s-no-outline'})
        product['url'] = 'https://www.amazon.in' + link['href']
        product['name'] = link.text.strip()
        
        price = result.find('span', {'class': 'a-price-whole'})
        if price:
            product['price'] = price.text.strip()
        else:
            product['price'] = ''
        
        rating = result.find('span', {'class': 'a-icon-alt'})
        if rating:
            product['rating'] = rating.text.strip().split()[0]
        else:
            product['rating'] = ''
        
        reviews = result.find('span', {'class': 'a-size-base', 'dir': 'auto'})
        if reviews:
            product['reviews'] = reviews.text.strip().replace(',', '')
        else:
            product['reviews'] = ''
        
        products.append(product)
    
    return products

# Scraping data from 20 pages
all_products = []

for i in range(1, 21):
    url = f'https://www.amazon.in/s?k=bags&page={i}'
    products = scrape_listing_page(url)
    all_products.extend(products)

# Part 2: Scraping additional data from each product page
def scrape_product_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    product = {}
    product['url'] = url
    
    asin = soup.find('th', {'class': 'a-color-secondary a-size-base prodDetAttrDesc'})
    if asin:
        product['asin'] = asin.find_next_sibling('td').text.strip()
    else:
        product['asin'] = ''
    
    product_desc = soup.find('div', {'id': 'productDescription'})
    if product_desc:
        product['description'] = product_desc.text.strip().replace('\n', ' ')
    else:
        product['description'] = ''
    
    manufacturer = soup.find('a', {'id': 'bylineInfo'})
    if manufacturer:
        product['manufacturer'] = manufacturer.text.strip()
    else:
        product['manufacturer'] = ''
    
    product.update(dict((k, '') for k in ['name', 'price', 'rating', 'reviews']))
    
    return product

# Scraping data from 200 product pages
final_data = []

for product in all_products[:200]:
    data = scrape_product_page(product['url'])
    data.update(product)
    final_data.append(data)

# Exporting data to a CSV file
with open('amazon_products.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=final_data[0].keys())
    writer.writeheader()
    writer.writerows(final_data)
