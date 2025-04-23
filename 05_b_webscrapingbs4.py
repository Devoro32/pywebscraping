# https://youtu.be/GjKQ6V_ViQE
# https://www.w3schools.com/cssref/css_selectors.php
# https://www.crummy.com/software/BeautifulSoup/bs4/doc/

import requests
from bs4 import BeautifulSoup as bs
import re
import pandas as pd

url = "https://keithgalli.github.io/web-scraping/"
r = requests.get(url + "webpage.html")

# convert to a beautiful soup objects
webpage = bs(r.content)
# print(webpage.prettify())

##rint(webpage.prettify())

print("--------------------------Social Link  1-------------------------------------")
"""
soclinks = webpage.select("ul.socials a")
print(soclinks)
(print("\n"))
actual_links = [link["href"] for link in soclinks]
print(actual_links)
(print("\n"))
"""
ulists = webpage.find("ul", attrs={"class", "socials"})
actual_links = ulists.find_all("a")

print(actual_links)

(print("\n"))
print("--------------------------Social Link  2-------------------------------------")
(print("\n"))
links = webpage.select("ul.socials a")
actual_links = [link["href"] for link in links]
print(actual_links)

(print("\n"))
print("--------------------------Social Link  3-------------------------------------")
(print("\n"))
links = webpage.select("li.social a")
actual_links = [link["href"] for link in links]
print(actual_links)


(print("\n"))
print("--------------------------Table-------------------------------------")
(print("\n"))
# ?https://stackoverflow.com/questions/50633050/scrape-tables-into-dataframe-with-beautifulsoup

table = webpage.select("table.hockey-stats")[0]
##print(table)
columns = table.find("thead").find_all("th")
columns_names = [c.string for c in columns]
##print(columns_name)
table_rows = table.find("tbody").find_all("tr")
l = []
for tr in table_rows:
    td = tr.find_all("td")
    row = [str(tr.get_text()).strip() for tr in td]
    l.append(row)
print(l[0])

df = pd.DataFrame(l, columns=columns_names)
print(df.head())

print(df["Team"])

print(df.loc[df["Team"] != "Did not play"])


(print("\n"))
print("--------------------------Fun Fact-------------------------------------")
(print("\n"))

facts = webpage.select("ul.fun-facts li")
facts_with_is = [fact.find(string=re.compile("is")) for fact in facts]
facts_with_is = [
    fact.findParent().get_text() for fact in facts_with_is if fact
]  # remove the 'none' within facts_with_is 'findParent()' will include the html tag
print(facts_with_is)


(print("\n"))
print("--------------------------Download Images-------------------------------------")
(print("\n"))

images = webpage.select("div.row div.column img")
image_url = images[0]["src"]
print(image_url)
fullimageurl = url + image_url
# https://stackoverflow.com/questions/30229231/python-save-image-from-url
img_data = requests.get(fullimageurl).content
with open("05_lake_como.jpg", "wb") as handler:
    handler.write(img_data)


(print("\n"))
print(
    "--------------------------Mystery Message Challenge-------------------------------------"
)
(print("\n"))
files = webpage.select("div.block a")
##print(files)
relative_files = [f["href"] for f in files]
print(relative_files)
for f in relative_files:
    full_url = url + f
    page = requests.get(full_url)
    bs_page = bs(page.content)
    # print(bs_page.body.prettify())
    secret_word_element = bs_page.find("p", attrs={"id": "sccret-word"})
    secret_word = secret_word_element.string
    print(secret_word)
