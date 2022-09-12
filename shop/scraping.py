import requests
from bs4 import BeautifulSoup
from shop.models import Product

# from time import sleep

# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.134 YaBrowser/22.7.1.802 Yowser/2.5 Safari/537.36",
#     "X-Amzn-Trace-Id": "Root=1-62e7c359-39d5cdc10e79f756776998ab"
#   }

# list_card_url = []


# def download(url):
#   resp = requests.get(url, stream=True)
#   r = open("C:\\Users\\rafik\\OneDrive\\Desktop\\image\\" + url.split("/")[-1], "wb")
#   for value in resp.iter_content(1024*1024):
#     r.write(value)
#   r.close()

class ScrapingError(Exception):
    pass


class ScrapingTimeoutError(ScrapingError):
    pass


class ScrapingHTTPError(ScrapingError):
    pass


class ScrapingOtherError(ScrapingError):
    pass

def get_url():
  for count in range(1,8):

    url = f"https://scrapingclub.com/exercise/list_basic/?page={count}"
    try:

        response = requests.get(url, timeout=10.0)  # , headers=headers

        # resp = requests.get(URL_SCRAPING, timeout=10.0)
    except requests.exceptions.Timeout:
        raise ScrapingTimeoutError("request timed out")
    except Exception as e:
        raise ScrapingOtherError(f'{e}')

    if response.status_code != 200:
        raise ScrapingHTTPError(f"HTTP {response.status_code}: {response.text}")


    soup = BeautifulSoup(response.text, "lxml") #html.parser
    data = soup.find_all("div", class_="col-lg-4 col-md-6 mb-4")

    for i in data:

      card_url = "https://scrapingclub.com" + i.find("a").get("href")
      yield card_url

def array():
  for card_url in get_url():
      response = requests.get(card_url) #  , headers=headers
      # sleep(1)
      soup = BeautifulSoup(response.text, "lxml") #html.parser
      data = soup.find("div", class_="card mt-4 my-4")
      name = data.find("h3", class_="card-title").text
      price = data.find("h4").text.replace("$", "")
      text = data.find("p", class_="card-text").text
      url_img = "https://scrapingclub.com" + data.find("img", class_="card-img-top img-fluid").get("src")
      #   download(url_img)
      # yield name, price, text, url_img
      print(name + "\n" + price + "\n" + text + "\n" + url_img + "\n\n")
       # for item in data_list:
      if not Product.objects.filter(name=name).exists():
        Product.objects.create(
        name=name,
        # code=item['code'],
        price=price,
        # unit=item['unit'],
        image_url=url_img,
        note=text,
      )

       # return data_list

if __name__ == '__main__':
    array()



# import re
# from decimal import Decimal
#
# import requests
# from bs4 import BeautifulSoup
#
# from main.settings import URL_SCRAPING_DOMAIN, URL_SCRAPING
#
# """
# {
#     'name': 'Труба профильная 40х20 2 мм 3м',
#     'image_url': 'https://my-website.com/30C39890-D527-427E-B573-504969456BF5.jpg',
#     'price': Decimal('493.00'),
#     'unit': 'за шт',
#     'code': '38140012'
#  }
# """
#
# def scraping():
#     resp = requests.get(URL_SCRAPING, timeout=10.0)
#     if resp.status_code != 200:
#         raise Exception('HTTP error access!')
#
#     data_list = []
#     html = resp.text
#     soup = BeautifulSoup(html, "lxml")  # 'html.parser'
#     blocks = soup.find_all("div", class_=".col-lg-4 col-md-6 mb-4")
#     for block in blocks:
#         data = {}
#         name = block.find("h4", class_="card-title").text.replace("\n", "")
#         price = block.find("h5").text
#         image_url = "URL_SCRAPING_DOMAIN" + block.find("img", class_="card-img-top img-fluid").get("src")
#         # print(name + "\n" + price + "\n" + image_url + "\n\n")
#         data['name'] = name
#         print(data)
# #         image_url = URL_SCRAPING_DOMAIN + block.select_one('img')['src']
# #         data['image_url'] = image_url
# #
# #         price_raw = name.select_one('.catalog-list .catalog-item .catalog-header--alt span')
# #         # '\r\n \t\t\t\t\t\t\t\t\t\t\t\t\t\t493.00\t\t\t\t\t\t\t\t\t\t\t\t  руб. '
# #         price = re.findall(r'\S\d+\.\d+\S', price_raw)[0]
# #         price = Decimal(price_raw)
# #         data['price'] = price   # 493.00
# #         #
# #         # unit = name.select_one('.unit ').text.strip()
# #         # # '\r\n \t\t\t\t\t\t\t\t\t\t\t\t\t\tза шт\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t'
# #         # data['unit'] = unit  # 'за шт'
# #         print(data)
# #
# # if __name__ == '__main__':
# #     scraping()
