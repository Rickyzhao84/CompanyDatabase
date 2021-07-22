import unittest
import requests
from bs4 import BeautifulSoup
import main
class TestMain(unittest.TestCase):
    def test_response_status_code(self):
        self.assertEqual(main.getResponseStatus(), 200)

    def test_Google_founder(self):
        response = requests.get(
            url="https://en.wikipedia.org/wiki/Google"
        )
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertTrue("Larry Page" in main.createTable(soup))

    def test_Microsoft_founder(self):
        response = requests.get(
            url = "https://en.wikipedia.org/wiki/Microsoft"
        )
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertTrue("Bill Gates" in main.createTable(soup))

    # def test_Netflix_founder(self):
    #     response = requests.get(
    #         url = "https://en.wikipedia.org/wiki/Netflix"
    #     )
    #     soup = BeautifulSoup(response.content, 'html.parser')
    #     self.assert_("Reed Hastings" in main.createTable(soup))

    def test_Apple_founder(self):
        response = requests.get(
            url="https://en.wikipedia.org/wiki/Apple_Inc."
        )
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertTrue("Steve Jobs" in main.createTable(soup))

    def test_Amazon_founder(self):
        response = requests.get(
            url="https://en.wikipedia.org/wiki/Amazon_(company)"
        )
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertTrue("Jeff Bezos" in main.createTable(soup))

    def test_Stripe_founder(self):
        response = requests.get(
            url="https://en.wikipedia.org/wiki/Stripe_(company)"
        )
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertTrue("John Collison" in main.createTable(soup))

    def test_Twitter_founder(self):
        response = requests.get(
            url="https://en.wikipedia.org/wiki/Twitter"
        )
        soup = BeautifulSoup(response.content, 'html.parser')
        self.assertTrue("Jack Dorsey" in main.createTable(soup))

if __name__ == '__main__':
    unittest.main()