# Libraries
import requests
import urllib.request
from time import time
from bs4 import BeautifulSoup

'''
    Functions
'''


def get_products_url(url, products):
    request = requests.get(url)
    category_Soup = BeautifulSoup(request.text, 'html.parser')
    data = category_Soup.select('h4 > a')
    for link in data:
        products.append(link['href'])


def save_product_data(file_path, product):
    with open(file_path, 'a') as file:
        line = '{0},{1},{2}\n'.format(product['title'],
                                      product['description'],
                                      product['model'])
        file.write(line)
        i = 0
        for image in product['images']:
            if (i == 0):
                path = 'images/' + product['model'].replace("/", "") + '.png'
                urllib.request.urlretrieve(image, path)
            else:
                path = 'images/' + product['model'] + '-' + str(i) + '.png'
                urllib.request.urlretrieve(image, path)
            i += 1
    file.closed


def get_product_data(url):
    request = requests.get(url)
    product_Soup = BeautifulSoup(request.text, 'html.parser')
    # Gets images
    images_data = product_Soup.select('.woocommerce-product-gallery__image >' +
                                      ' a[href]')
    images = list()
    for data in images_data:
        images.append(data['href'])
    # Gets title
    title = product_Soup.select('.product_title')
    title = title[0].text
    # Gets description
    description = product_Soup.select('.description')
    description = description[0].text
    # Gets Model (SKU)
    model = product_Soup.select('.sku')
    model = model[0].text
    # Builds the product
    product = dict(images=images, title=title, description=description,
                   model=model)
    # Saves the product data
    save_product_data('products.csv', product)
    # Mark the product as processed
    with open('processed.txt', 'a') as file:
        line = url + "\n"
        file.write(line)
    file.closed


# Set initial URL
url = 'http://www.mitzu.com/productos/'

# Retrieves already processed products
processed = list()
with open('processed.txt', 'r') as file:
    processed = file.readlines()
file.closed

# Initial request
request = requests.get(url)
soup = BeautifulSoup(request.text, 'html.parser')

# Gets all categories
categories = list()
for link in soup.find_all('a', class_='vc_single_image-wrapper'):
    categories.append(link['href'])

# Gets all products from each category
products_links = list()
for category in categories:
    print("Category: " + category)
    url = category + "?product_count=400"
    get_products_url(url, products_links)

# Gets and save the data from each product
for url in products_links:
    # Check is the product has already been processed
    if (url + "\n" in processed):
        print('Skipped: ' + url)
        continue
    else:
        print("Product: " + url)
        get_product_data(url)
