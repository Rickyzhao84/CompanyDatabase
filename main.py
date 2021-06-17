import requests
from bs4 import BeautifulSoup
import pandas as pd


response = requests.get(
url="https://en.wikipedia.org/wiki/Google"
)
table_name = 'wikitable sortable'
soup = BeautifulSoup(response.content, 'html.parser')



#Get the table that has Company Name
def getCompanyName():
    array = soup.find_all('table')
    for key in array:
        if ("Founders" in key.prettify()):
            results = soup.find('td', class_='infobox-data')
            return results.prettify()
    return 0

print(getCompanyName())

def createTable(soup):
    table = soup.find('table', {'class':"infobox vcard"})
    df = pd.read_html(str(table))
    df = pd.DataFrame(df[0])
    print(df)
    return getFounders(df)

def getFounders(df):
    for index, row in df.iterrows():
        if ("Founders" in row[0] or "Founder" in row[0] or "Founder(s)" in row[0]):
            print(row[1])
            return row[1]


createTable(soup)


def getResponseStatus():
    return response.status_code

#https://www.geeksforgeeks.org/web-scraping-from-wikipedia-using-python-a-complete-guide/