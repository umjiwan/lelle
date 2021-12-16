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

    def code(self):
        selector = "#content > div.section_search > table > tbody > tr:nth-child(1) > td.tit > a"
        code = (self.soup).select_one(selector)
        return str(code)[31:37]

    def price(self):
        selector = "2)"
        price = (self.soup).select_one(self.base_selector + selector)
        return price.text

    def compare(self):
        selector = "3)"
        compare = (self.soup).select_one(self.base_selector + selector)
        
        if str(compare)[30:32] != "상승":
            return int(compare.text) * -1

        return int(compare.text)
        
    def fluctuating(self):
        selector = "4)"
        fluctuating = (self.soup).select_one(self.base_selector + selector)
        return fluctuating.text

    def sellask(self):
        selector = "5)"
        sellask = (self.soup).select_one(self.base_selector + selector)
        return sellask.text

    def buyask(self):
        selector = "6)"
        buyask = (self.soup).select_one(self.base_selector + selector)
        return buyask.text

    def transaction(self):
        selector = "7)"
        transaction = (self.soup).select_one(self.base_selector + selector)
        return transaction.text