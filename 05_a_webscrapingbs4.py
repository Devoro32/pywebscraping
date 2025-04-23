# https://youtu.be/GjKQ6V_ViQE
# https://www.w3schools.com/cssref/css_selectors.php
# https://www.crummy.com/software/BeautifulSoup/bs4/doc/

import requests
from bs4 import BeautifulSoup as bs
import re

# load the webpage content

r = requests.get("https://keithgalli.github.io/web-scraping/example.html")

# convert to a beautiful soup objects
soup = bs(r.content)

# print out our html
print(soup.prettify())

print("----------------------------------------------------------------------------")
# find - will find the first element, find_all- will find all the element within the html
first_header = soup.find("h2")
print(first_header)
headers = soup.find_all("h2")
print(headers)

# Pass in a list of element to look for
first_header = soup.find("h1", "h2")  # order does not matter, it will get the first one

headers = soup.find_all(["h1", "h2"])
print(headers)

(print("\n"))
print("--------------------------_Attritributes-------------------------------------")
(print("\n"))
paragraph = soup.find_all("p")
print(paragraph)

paragraphid = soup.find_all("p", attrs={"id": "paragraph-id"})
print("paragraph id:" + str(paragraphid))
(print("\n"))
print("--------------------------Nested Div-------------------------------------")
(print("\n"))
body = soup.find("body")
div = body.find("div")
header = div.find("h1")
print("nested find: " + str(header))

(print("\n"))
print(
    "--------------------------Find specific string----------------------------------"
)
(print("\n"))
parastring = soup.find_all("p", string=re.compile("some"))  # regEx expression to find

print(parastring)
headers = soup.find_all("h2", string=re.compile("(h|H)eader"))
print(headers)

(print("\n"))
print("--------------------------Div----------------------------------")
(print("\n"))
content = soup.select("div p")
print(content)

paraidiv = soup.select("h2 ~ p")
print(paraidiv)

bold_text = soup.select("p#paragraph-id b")
print(bold_text)

paragsels = soup.select("body > p")
print(paragsels)

for parag in paragsels:
    print(parag.select("i"))

(print("\n"))
print("--------------------------Element- MIDDLE----------------------------------")
(print("\n"))
# grap by element with specific property
print(soup.select("[align=middle]"))


(print("\n"))
print("--------------------------Get String----------------------------------")
(print("\n"))

header = soup.find("h2")
print(header.string)  # strip the h2 tag

div = soup.find("div")
print(div.prettify())
# TODO: This is what we need to use for novelbin to export to txt
print(div.get_text())  # get the data rather than the tags
print("--------------------------Specific element----------------------------------")
(print("\n"))
# Get a specific property from an element
linkhref = soup.find("a")
print(linkhref["href"])

paragid = soup.select("p#paragraph-id")
print(paragid[0]["id"])


(print("\n"))

print("--------------------------Syntax element----------------------------------")
(print("\n"))
print(soup.body.prettify())
# Path syntax
print(soup.body.div.h1.string)
# Know the terms: parent, sibling, child

sibling = soup.body.find("div").find_next_sibling
print("SIBLING: ")
print(sibling)
