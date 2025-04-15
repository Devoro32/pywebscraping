# python -m venv env to create a virtual environment
# pip3 install httpx
# pip install selectolax
# https://youtu.be/1PCWwK0AsE0?list=PLRzwgpycm-FiTz9bGQoITAzFEOJkbF6Qp
from requests import Response
import httpx
from selectolax.parser import HTMLParser

url = "https://books.toscrape.com/"
# url ='https://www.rei.com/c/camping-and-hiking/f/scd-deals'
header = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
}  # find my searching 'my user agent' on google'

respn = httpx.get(url, headers=header)
"""
if respn.status_code == 200:
  html_content = respn.text
  #print(html_content)
else:
  print("Failed to fetch the webpage.")
"""
# print(respn.text)# convert to html
"""html = HTMLParser(html_content)"""
html = HTMLParser(respn.text)

# print(html)
##print(html.css_first('title'))# get the first title which would be Node Title /Object thus we need to assign text to it


# if the selector does not exist it will return an error, thus we need to add a try catch
def extract_text(html, sel):
    try:
        return html.css_first(sel).text()
    except AttributeError:
        return None


##print(html.css_first('title').text())

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
    print(item)
