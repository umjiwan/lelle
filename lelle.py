# maby ul

from urllib import parse
from bs4 import BeautifulSoup
import requests
import re

class stock:
    def __init__(self, name):

        if name == "카카오":
            name = "kakao"

        base_url = "https://finance.naver.com/search/searchList.naver?query="
        suffix = parse.quote(name.encode("euc-kr"))

        url = base_url + suffix

        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        # base_selector = "#content > div.section_search > table > tbody > tr:nth-child(1) > td:nth-child("
        
        selector = "#content > div.section_search > table > tbody > tr:nth-child(1) > td.tit > a"
        st_code = str(soup.select_one(selector))[31:37]

        url = "https://finance.naver.com/item/main.naver?code=" + st_code
        
        response = requests.get(url)
        html = response.text
        soup = BeautifulSoup(html, "html.parser")

        updown_select = "div > p.no_today"
        updown_code = str(soup.select_one(updown_select))

        updown = re.findall(r"<em class=\".+", updown_code)[0]
        updown = updown[11:-2]

        self.updown = updown
        self.soup = soup
        self.st_code = st_code
        # self.base_selector = base_selector

    def name(self):
        selector = "#middle > div.h_company > div.wrap_company > h2 > a"
        name = (self.soup).select_one(selector)
        return name.text

    def code(self):
        return self.st_code

    def price(self):
        selector = f"div > p.no_today > em.{self.updown} > span.blind"
        price = (self.soup).select_one(selector)
        return price.text

    def compare(self):
        selector = f"div > p.no_exday > em.{self.updown} > span.blind"
        compare = (self.soup).select_one(selector).text

        ics_selector = f"div > p.no_exday > em.{self.updown} > span"
        increase = (self.soup).select_one(ics_selector).text

        if increase != "상승":
            compare = f"-{compare}"
        else:
            compare = f"+{compare}"

        return compare
        
    def pe_compare(self):
        pm_selector = "#chart_area > div.rate_info > div > p.no_exday > em:nth-child(4) > span"
        pm = (self.soup).select_one(pm_selector).text

        sh_selector = pm_selector + ".blind"
        sh = (self.soup).select_one(sh_selector).text

        return pm + sh + "%"

class ulang:
    def __init__(self, sentence):
        binary = "".join(format(c, 'b') for c in bytearray(sentence, "utf-8"))
        binary_list = list(binary)

        self.sentence = sentence
        self.binary = binary
        self.binary_list = binary_list

    def encryption(self):
        change_list = []

        for count in self.binary_list:
            if count == "0":
                change_list.append("u")
            elif count == "1":
                change_list.append("l")

        ul_sentence = "".join(change_list)
        
        return ul_sentence