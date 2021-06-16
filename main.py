import requests
from bs4 import BeautifulSoup
import pandas as pd

response = requests.get(
    url = "https://en.wikipedia.org/wiki/Google"
)
table_name = 'wikitable sortable'
soup = BeautifulSoup(response.content, 'html.parser')

print(soup.find_all('table')[0].get_text())
print(soup.find_all('table')[1].get_text())




print('\n\n')


def getResponseStatus():
    return response.status_code

#https://www.geeksforgeeks.org/web-scraping-from-wikipedia-using-python-a-complete-guide/