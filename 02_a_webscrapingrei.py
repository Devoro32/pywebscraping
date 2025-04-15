# python -m venv env to create a virtual environment
# pip3 install httpx
# pip install selectolax

from requests import Response
import httpx
from selectolax.parser import HTMLParser

url = "https://www.rei.com/c/camping-and-hiking/f/scd-deals"
header = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
}  # find my searching 'my user agent' on google'

respn = httpx.get(url, headers=header)

html = HTMLParser(respn.text)

##print(html.css_first('title'))# get the first title which would be Node Title /Object thus we need to assign text to it


# if the selector does not exist it will return an error, thus we need to add a try catch
def extract_text(html, sel):
    try:
        return html.css_first(sel).text()
    except AttributeError:
        return None


##print(html.css_first('title').text())

products = html.css("li.VcGDfKKy_dvNbxUqm29K")  # for id #, class= .

for product in products:
    item = {
        #'name': product.css_first('h3 a').text(),
        "name": extract_text(product, ".Xpx0MUGhB7jSm5UvK2EY"),
        #'price': product.css_first('p.price_color').text(),
        "price": extract_text(product, "span[data-ui=sale-price]"),
    }
    print(item)
