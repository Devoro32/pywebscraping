import requests
import bs4

# https://youtu.be/b8q98xvyIqg
base_url = "https://xkcd.com"
url = "https://xkcd.com/1"


while "#" not in url:

    response = requests.get(url)

    # ---------------------------------Part 1: Request and soupify------------------------------------------------
    # request the webpage
    # print(response) #<response [200]>
    # print(response.content) #body of the html

    # parse the page to make it easy to use
    soup = bs4.BeautifulSoup(
        response.content, "html.parser"
    )  # create a tree of the html, ever node will be on its own line. It will look like html preformatted
    ##print(soup)
    # ---------------------------------Part 2:  Find the URL of the image-----------------------------------------

    img_element = soup.select("#comic img")[
        0
    ]  # looking at the CSS for id comic and within the div get the image
    ##print(img_element)
    # <div id="comic"><img src="//imgs.xkcd.com/comics/tariffs.png" ...
    # returning the first element of the list

    img_src = img_element["src"]  # want to extract the source of the image
    ##print(img_src)

    img_src = "http:" + str(img_src)

    # Get the name of the file
    print("file name: " + img_src.split("/")[-1])
    img_name = img_src.split("/")[-1]

    # convert this into a string and add http to the front otherwise it will think of the img_src as a list

    print("url: " + img_src)

    # ---------------------------------Part 3:  download the image-----------------------------------------
    reponse = requests.get(img_src)

    # send a HTTP request to the serve and save
    # the HTTP response in a response object called r
    with open("comics/" + img_name, "wb") as file:  # wb=> write bytes
        # Saving received content as a png file in
        # binary format
        # write the content of the response (r.content)
        # to a new file in  a binary mode
        file.write(response.content)

    # ---------------------------------Part 4:  Find the next button-----------------------------------------
    ##print(soup.select(".comicNav a[rel='next']"))

    next_a = soup.select(".comicNav a[rel='next']")[0]

    next_href = next_a["href"]
    print("href " + str(next_href))
    url = base_url + str(next_href)
    print("new url " + url)

"""
https://youtu.be/vxk6YPRVg_o
web scraping tools: puppetter, playwrite, selium
scraping browswer
bright data company that has: web unlocker

"""
