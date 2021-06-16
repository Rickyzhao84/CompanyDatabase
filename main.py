import requests

response = requests.get(
    url = "https://en.wikipedia.org/wiki/Google",
)

print(response.status_code);

print(response.content);

#https://www.geeksforgeeks.org/web-scraping-from-wikipedia-using-python-a-complete-guide/