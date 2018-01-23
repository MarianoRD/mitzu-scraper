# Libraries
import requests
import urllib.request
from bs4 import BeautifulSoup

'''
    Functions
'''


def get_products_url(url):
    products_temp = list()
    request = requests.get(url)
    category_Soup = BeautifulSoup(request.text, 'html.parser')
    data = category_Soup.select('h4 > a')
    for link in data:
        products_temp.append(link['href'])

    return products_temp


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
    description = product_Soup.select('.description > p')
    description = description[0].text
    # Gets Model (SKU)
    model = product_Soup.select('.sku')
    model = model[0].text
    # Builds the product
    product = dict(images=images, title=title, description=description,
                   model=model)
    print(product)

    return product


def save_product_data(file_path, products):
    with open(file_path, 'a') as file:
        for product in products:
            file.write('{0},{1},{2}\n'.format(product['title'],
                                              product['description'],
                                              product['model']))
            i = 0
            for image in product['images']:
                if (i == 0):
                    urllib.request.urlretrieve(image, product['model'] +
                                               '.png')
                else:
                    urllib.request.urlretrieve(image, product['model'] + '-'
                                               + i + '.png')
                i += 1
    file.closed


# Set initial URL
url = 'http://www.mitzu.com/productos/'

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
    products_links.append(get_products_url(url))

# Gets the data from each product
products = list()
for product in products_links:
    print("Product: " + product)
    products.append(get_product_data(url))

# Save the data of the products

# Save text in CSV
# Save images
