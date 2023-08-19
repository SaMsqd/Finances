import pandas as pd
import requests
from bs4 import BeautifulSoup
import pandas


def cut(string):
    return str(int(string) / 100)


def create_url(request: str):
    return f"https://search.wb.ru/exactmatch/ru/common/v4/search?TestGroup=no_test&TestID=no_test&appType=1&curr" \
           f"=rub&dest=-1257786&query=%{request}&regions=80,38,83,4,64,33,68,70,30,40,86,75,69,1,31,66,22,110,48," \
           f"71,114&resultset=catalog&sort=popular&spp=0&suppressSpellcheck=false"


def get_cards(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:102.0) Gecko/20100101 Firefox/102.0",
        "Accept": "*/*",
        "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https;//www.wildberries.ru/",
        "Origin": "https://www.wildberries.ru",
        "Connection": "keep-alive",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
    }
    return requests.get(url=url, headers=headers).json()


def get_products(response):
    result = []
    products = response.get("data", {}).get("products", None)
    print(products)
    if products is not None:
        n = 0
        for product in products:
            n += 1
            result.append(
                {
                    "Артикул": product.get("id", None),
                    "Наименование": product.get("name", "Ошибка"),
                    "Брэнд": product.get("brand", "Ошибка"),
                    # "Изначальная цена": cut(product.get("priceU", "Ошибка")),
                    # "Цена с акцией": cut(product.get("salePriceU", "Ошибка(акции нет)")),
                    # "Отзывы": str(product.get("reviewRating")) + " звёзд",
                    # "Количество отзывов": product.get("feedbacks", "Ошибка")
                }
            )
            if n == 10:
                break
    return result


if __name__ == "__main__":
    #get_products(get_cards(create_url("памперсы")))
    pd.DataFrame(get_products(get_cards(create_url("памперсы")))).to_csv("products.csv", index=False)
