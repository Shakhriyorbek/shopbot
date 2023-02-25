import requests
from bs4 import BeautifulSoup

class Parser:
    def __init__(self):
        self.url = 'https://olcha.uz/ru/'
        self.host = 'https://olcha.uz'
        self.data = {}

    def get_html(self, url=None):
        if url:
            html = requests.get(url).text
        else:
            html = requests.get(self.url).text
        return html

    def get_soup(self, html):
        return BeautifulSoup(html, 'html.parser')


    def get_data(self):
        soup = self.get_soup(self.get_html('https://olcha.uz/ru/category/dlya-geymerov'))
        grid = soup.find('div', class_='grid-cols-5')
        categories = grid.find_all('a', class_='block')
        for category in categories:
            title = category.find('p').get_text(strip=True)
            print(title)
            self.data[title] = []
            category_link = self.host + category.get('href')
            category_soup = self.get_soup(self.get_html(category_link))
            products = category_soup.find_all('div', class_='w-52')
            for product in products:
                try:
                    product_title = product.find('p', class_='h-12').get_text(strip=True)
                    product_price = int(product.find('span', class_='text-lg').get_text(strip=True).replace(' ', ''))
                    product_image_link = product.find('img').get('src')
                    product_link = self.host + product.find('a', class_='absolute').get('href')
                    product_soup = self.get_soup(self.get_html(product_link))
                    product_description = product_soup.find('p', class_='break-words').get_text(strip=True)
                    self.data[title].append({
                        'product_title': product_title,
                        'product_price': product_price,
                        'product_description': product_description,
                        'product_image_link': product_image_link,
                        'product_link': product_link
                    })
                except:
                    continue
        return self.data

