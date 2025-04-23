# python -m venv env to create a virtual environment
# pip3 install httpx
# pip install selectolax
#! https://youtu.be/r7pMqU2kYqc?list=PLRzwgpycm-FiTz9bGQoITAzFEOJkbF6Qp
from requests import Response
import httpx
from selectolax.parser import HTMLParser
import time
from urllib.parse import urljoin
from dataclasses import asdict, dataclass, fields
import json
import csv


@dataclass
class Item:
    name: str | None
    item_num: str | None
    price: str | None
    rating: float | None


def get_html(url, **kwargs):

    print(kwargs.get("page"))  # ? use get so if there is an error it wont hurt the code
    # add **kwargs so you don't have to pass a default

    header = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0       Safari/537.36"
    }  # find my searching 'my user agent' on google'
    if kwargs.get("page"):
        respn = httpx.get(
            url + str(kwargs.get("page")), headers=header, follow_redirects=True
        )
    else:
        respn = httpx.get(url, headers=header, follow_redirects=True)
    # follow_redirects=True will follow the redirect to the new url
    ##print(respn.status_code) # 301 means a redirect
    try:  # check if the status code is 200, if not it will raise an error
        respn.raise_for_status()  # if the status code is not 200, it will raise an error
    except httpx.HTTPStatusError as exc:
        print(
            f"Error response {exc.response.status_code} while requesting {exc.request.url!r}.  Page limit exceeded"
        )
        return False

    html = HTMLParser(respn.text)
    return html

    ##print(html.css_first('title'))# get the first title which would be Node Title /Object thus we need to assign text to it


# if the selector does not exist it will return an error, thus we need to add a try catch
def extract_text(html, sel):
    try:

        text = html.css_first(sel).text()
        return clean_data(text)  # cleaning and returning the text at the same time
    except AttributeError:
        return None


def export_to_json(products):
    with open(
        "product.json", "w", encoding="utf-8"
    ) as f:  # encoding to fit a certain format
        json.dump(
            products, f, ensure_ascii=False, indent=4
        )  #'f' indicate you are dumping into a file, additional formating using ensure and indent
    print("Saved to json")


def export_to_csv(products):
    field_names = [
        field.name for field in fields(Item)
    ]  # ?access to fields of data within the data class, not from the data exported
    with open("product.csv", "w") as f:
        writer = csv.DictWriter(f, field_names)
        writer.writeheader()
        writer.writerows(products)
    print("Saved to csv")


def append_to_csv(products):
    field_names = [field.name for field in fields(Item)]
    with open("appendcsv.csv", "a") as f:
        writer = csv.DictWriter(f, field_names)
        writer.writerows(products)


def parse_search_page(html: HTMLParser):
    products = html.css("li.VcGDfKKy_dvNbxUqm29K")  # for id #, class= .

    for product in products:

        # get the URl of each product and then we will be going toward it
        yield urljoin("https://www.rei.com", product.css_first("a").attributes["href"])


def parse_item_page(html: HTMLParser):
    new_item = Item(
        name=extract_text(html, "h1#product-page-title"),
        item_num=extract_text(html, "span#product-item-number"),
        price=extract_text(html, "span#buy-box-product-price"),
        rating=extract_text(html, "span.cdr-rating__number_13-5-3"),
    )
    return asdict(new_item)  # converting the dataclass back into a dictionary


def clean_data(value):
    chars_to_remove = ["$", "Item", "#"]
    for char in chars_to_remove:
        if char in value:
            value = value.replace(char, "")
    return value.strip()


def main():
    products = []
    baseurl = "https://www.rei.com/c/camping-and-hiking/f/scd-deals?page="  # add the '?page=' for the pagination
    for x in range(1, 30):  # up to 10 pages, not including 10
        print(f"Gathering page: {x}")

        html = get_html(baseurl, page=x)
        time.sleep(1)
        if html is False:
            break
        product_urls = parse_search_page(html)

        for url in product_urls:
            print("Url:" + url)
            html = get_html(url)
            products.append(parse_item_page(html))
            time.sleep(0.1)


if __name__ == "__main__":
    main()
