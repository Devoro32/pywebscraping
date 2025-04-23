# https://youtu.be/DcI_AZqfZVc
import requests
from bs4 import BeautifulSoup as bs
import json

#! Not finish, issue
"""Failed to process URL https://walmart.com/ip/HP-Stream-14-inch-Laptop-Intel-Processor-N4102-4GB-RAM-64GB-eMMC-Pink-12-mo-Microsoft-365-included/443153637?classType=undefined&variantFieldId=actual_color. Error 'NoneType' object has no attribute 'string'
Failed to process URL https://walmart.com/ip/HP-Stream-14-inch-Laptop-Intel-Processor-N4102-4GB-RAM-64GB-eMMC-Blue-12-mo-Microsoft-365-included/166773164?classType=undefined&variantFieldId=actual_color. Error 'NoneType' object has no attribute 'string'
Search page2"""

walmart_url = "https://www.walmart.com/ip/LG-32-Ultra-Gear-QHD-2560-x-1440-Gaming-Monitor-165Hz-1ms-Black-32GN600-B-Aus-New/406688031?classType=REGULAR&athbdg=L1103"

HEADERS = {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-GB,en;q=0.9",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
}


def get_product_links(query, page_number=1):
    search_url = f"https://www.walmart.com/search?q={query}&page={page_number}"

    print(search_url)

    response = requests.get(search_url, headers=HEADERS)
    soup = bs(response.text, "html.parser")
    links = soup.find_all("a", href=True)

    product_links = []

    for link in links:
        link_href = link["href"]
        if "/ip/" in link_href:
            if "https" in link_href:
                full_url = link_href
            else:
                full_url = "https://walmart.com" + link_href

            product_links.append(full_url)

    return product_links


def extract_product_info(product_url):
    response = requests.get(product_url, headers=HEADERS)

    # html = response.text
    soup = bs(response.text, "html.parser")

    script_tag = soup.find("script", id="__NEXT_DATA__")
    # html = script_tag

    # can find the header within Network => Fetch/XHR => collector  =>
    # print(html)

    data = json.loads(
        script_tag.string
    )  # convert the data to json because the html had over 5k token via token counter
    """ 

    # print(data.keys())
    print(
        data["props"]["pageProps"]["initialData"]["data"]["product"]["priceInfo"][
            "currentPrice"
        ]["price"]
    )
    """
    initial_data = data["props"]["pageProps"]["initialData"]["data"]
    product_data = initial_data["product"]
    reviews_data = initial_data.get("reviews", {})
    product_info = {
        "price": product_data["priceInfo"]["currentPrice"]["price"],
        "review_count": reviews_data.get("totalReviewCount", 0),
        "item_id": product_data["usItemId"],
        "avg_rating": reviews_data.get("averageOverallRating", 0),
        "product_name": product_data["name"],
        "brand": product_data.get("brand", ""),
        "availability": product_data["availabilityStatus"],
        "image_url": product_data["imageInfo"]["thumbnailUrl"],
        "short_description": product_data.get("shortDescription", ""),
    }

    return product_info


def main():
    # print(get_product_links("computers"))

    OUTPUT_FILE = "05_product_info.json"
    page_number = 1
    with open(OUTPUT_FILE, "w") as file:
        while True:
            links = get_product_links("computers", page_number)
            if not links or page_number > 99:
                break

            for link in links:
                try:
                    product_info = extract_product_info(link)
                    if product_info:
                        file.write(json.dumps(product_info) + "\n")
                except Exception as e:
                    print(f"Failed to process URL {link}. Error {e}")

            page_number += 1
            print(f"Search page{page_number}")


if __name__ == "__main__":
    main()
