# python -m venv env to create a virtual environment
# pip3 install httpx
# pip install selectolax
# https://youtu.be/ZgVus_rmDBQ?list=PLRzwgpycm-FiTz9bGQoITAzFEOJkbF6Qp
from requests import Response
import httpx
from selectolax.parser import HTMLParser
import time


def get_html(base_url, page):

    header = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0       Safari/537.36"
    }  # find my searching 'my user agent' on google'

    respn = httpx.get(base_url + str(page), headers=header, follow_redirects=True)
    # follow_redirects=True will follow the redirect to the new url
    ##print(respn.status_code) #301 means a redirect
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


def parse_page(html):
    products = html.css("li.VcGDfKKy_dvNbxUqm29K")  # for id #, class= .

    for product in products:

        item = {
            #'name': product.css_first('h3 a').text(),
            "name": extract_text(product, ".Xpx0MUGhB7jSm5UvK2EY"),
            #'price': product.css_first('p.price_color').text(),
            "price": extract_text(product, "span[data-ui=sale-price]"),
            "saving": extract_text(product, "div[data-ui=savings-percent-variant2]"),
        }
        ##print(item)
        yield item


def main():
    baseurl = "https://www.rei.com/c/camping-and-hiking/f/scd-deals?page="  # add the '?page=' for the pagination
    for x in range(1, 30):  # up to 10 pages, not including 10
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
