# maby ul

from urllib import parse
from bs4 import BeautifulSoup
import requests

class stock:
    def __init__(self, name):
        base_url = "https://finance.naver.com/search/searchList.naver?query="
        suffix = parse.quote(name.encode("euc-kr"))

        url = base_url + suffix

        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        base_selector = "#content > div.section_search > table > tbody > tr:nth-child(1) > td:nth-child("

        self.soup = soup
        self.base_selector = base_selector


    def name(self):
        selector = "1)"
        name = (self.soup).select_one(self.base_selector + selector)
        return name.text[:-2]

    def price(self):
        pass

    def compare(self):
        pass

    def fluctuating(self):
        pass

    def sellask(self):
        pass

    def buyask(self):
        pass

    def transaction(self):
        pass