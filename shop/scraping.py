import requests
from bs4 import BeautifulSoup
from shop.models import Product


class ScrapingError(Exception):
    pass


class ScrapingTimeoutError(ScrapingError):
    pass


class ScrapingHTTPError(ScrapingError):
    pass


class ScrapingOtherError(ScrapingError):
    pass


def get_url():
    for count in range(1, 8):

        url = f"https://scrapingclub.com/exercise/list_basic/?page={count}"
        try:

            response = requests.get(url, timeout=10.0)  # , headers=headers

            # resp = requests.get(URL_SCRAPING, timeout=10.0)
        except requests.exceptions.Timeout:
            raise ScrapingTimeoutError("request timed out")
        except Exception as e:
            raise ScrapingOtherError(f'{e}')

        if response.status_code != 200:
            raise ScrapingHTTPError(
                f"HTTP {response.status_code}:{response.text}")

        soup = BeautifulSoup(response.text, "lxml")  # html.parser
        data = soup.find_all("div", class_="col-lg-4 col-md-6 mb-4")

        for i in data:
            card_url = "https://scrapingclub.com" + i.find("a").get("href")
            yield card_url


def array():
    for card_url in get_url():
        response = requests.get(card_url)  # , headers=headers
        # sleep(1)
        soup = BeautifulSoup(response.text, "lxml")  # html.parser
        data = soup.find("div", class_="card mt-4 my-4")
        name = data.find("h3", class_="card-title").text
        price = data.find("h4").text.replace("$", "")
        text = data.find("p", class_="card-text").text
        url_img = "https://scrapingclub.com" + \
                  data.find("img", class_="card-img-typing-fluid").get("src")
        print(name + "\n" + price + "\n" + text + "\n" + url_img + "\n\n")
        if not Product.objects.filter(name=name).exists():
            Product.objects.create(
                name=name,
                # code=item['code'],
                price=price,
                # unit=item['unit'],
                image_url=url_img,
                note=text,
            )


if __name__ == '__main__':
    array()



