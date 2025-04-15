import requests
from bs4 import BeautifulSoup

url = "https://books.toscrape.com/"

respn = requests.get(url)

soup = BeautifulSoup(respn.text, "html.parser")
categlogue = soup.select("article", class_="product_pod")

for book in categlogue:
    # title
    if book.h3.a:
        title = book.h3.a["title"]
    else:
        title = "No title found"
    # price
    if book.find("p", class_="price_color"):
        price = book.find("p", class_="price_color").get_text().strip()
    else:
        price = "No price found"
    # rating
    if book.find("p", class_="star-rating"):
        rating = book.find("p", class_="star-rating")["class"][1]
    else:
        rating = "No rating found"
    if book.find("p", class_="instock availability"):
        availability = book.find("p", class_="instock availability").text.strip()
    else:
        availability = "No data found"

    print("Title: ", title)
    print("price: ", price)
    print("Rating", rating)
    print("Availability", availability)
