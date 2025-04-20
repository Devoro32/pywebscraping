# python -m venv env to create a virtual environment
# pip3 install httpx
# pip install selectolax
# https://youtu.be/ZgVus_rmDBQ?list=PLRzwgpycm-FiTz9bGQoITAzFEOJkbF6Qp
from requests import Response
import httpx
from selectolax.parser import HTMLParser
import time

#! new import
from urllib.parse import urljoin
from dataclasses import asdict, dataclass


@dataclass
class Item:
    name: str | None
    item_num: str | None
    price: str | None
    rating: float | None


def get_html(url, **kwargs):
    #! added this new section
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
        return html.css_first(sel).text()
    except AttributeError:
        return None


##print(html.css_first('title').text())


def parse_search_page(html: HTMLParser):
    products = html.css("li.VcGDfKKy_dvNbxUqm29K")  # for id #, class= .

    for product in products:
        #! added this new section
        # get the URl of each product and then we will be going toward it
        yield urljoin("https://www.rei.com", product.css_first("a").attributes["href"])


def parse_item_page(html: HTMLParser):
    new_item = Item(
        name=extract_text(html, "h1#product-page-title"),
        item_num=extract_text(html, "span#product-item-number"),
        price=extract_text(html, "span#buy-box-product-price"),
        rating=extract_text(html, "span.cdr-rating__number_13-5-3"),
    )
    return new_item


def main():
    products = []
    baseurl = "https://www.rei.com/c/camping-and-hiking/f/scd-deals?page="  # add the '?page=' for the pagination
    for x in range(1, 30):  # up to 10 pages, not including 10
        print(f"Gathering page: {x}")
        #! updated this section
        html = get_html(baseurl, page=x)
        time.sleep(1)
        if html is False:
            break
        product_urls = parse_search_page(html)
        for url in product_urls:
            #! added this new section
            html = get_html(url)
            print(html.css_first("title").text())  # getting the title
            products.append(parse_item_page(html))
            time.sleep(1)
    for product in products:
        print(asdict(product))  # asdict will produces the dictionary item


if __name__ == "__main__":
    main()
