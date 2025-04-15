# python -m venv env to create a virtual environment
# pip3 install httpx
# pip install selectolax
# https://youtu.be/1PCWwK0AsE0?list=PLRzwgpycm-FiTz9bGQoITAzFEOJkbF6Qp
from requests import Response
import httpx
from selectolax.parser import HTMLParser
import time


def get_html(base_url, page):

    header = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
    }  # find my searching 'my user agent' on google'
    newpage = f"page-{page}.html"
    print("New page: " + base_url + newpage)
    respn = httpx.get(base_url + newpage, headers=header, follow_redirects=True)
    try:
        respn.raise_for_status()
    except httpx.HTTPStatusError as exc:
        print(
            f"Error response {exc.response.status_code} while requesting {exc.request.url!r}.  Page limit exceeded"
        )
        return False
    html = HTMLParser(respn.text)
    return html


# if the selector does not exist it will return an error, thus we need to add a try catch
def extract_text(html, sel):
    try:
        return html.css_first(sel).text()
    except AttributeError:
        return None


##print(html.css_first('title').text())


def parse_page(html):

    books = html.css(".product_pod")  # for id #, class= .
    # print(books)
    for book in books:
        print(book)
        item = {
            #'name': product.css_first('h3 a').text(),
            "name": extract_text(book, "a[title]"),
            #'price': product.css_first('p.price_color').text(),
            "price": extract_text(book, "p.price_color"),
        }
        # print(item)
        yield item


def main():
    baseurl = "https://books.toscrape.com/catalogue/"
    for x in range(1, 3):
        print(f"Gathering page: {x}")
        html = get_html(baseurl, x)
        time.sleep(1)
        if html is False:
            break
        data = parse_page(html)
        for item in data:
            print(item)


if __name__ == "__main__":
    main()
