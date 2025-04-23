from bs4 import BeautifulSoup as bs
import requests
import lxml

html_text = requests.get(
    "https://m.timesjobs.com/mobile/jobs-search-result.html?jobsSearchCriteria=Sales+%26+Marketing&cboPresFuncArea=32"
)

soup = bs(html_text.content, "lxml")
# print(soup)
jobs = soup.find("li")
print(jobs)
