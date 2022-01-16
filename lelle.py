# maby ul

from unicodedata import decimal
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
        self.sentence = sentence

    def encryption(self):
        binary = str(" ".join(format(c, 'b') for c in bytearray(self.sentence, "utf-8")))
        binary_list = list(binary)
        change_list = []

        for i in binary_list:
            if i == "0":
                change_list.append("u")
            elif i == "1":
                change_list.append("l")
            elif i == " ":
                change_list.append(" ")
                
        result = "".join(change_list)
        return result

"""    def decryption(self):
        list_sentence = list(self.sentence)
        ulang_list =[]

        for i in list_sentence:
            if i == "u":
                ulang_list.append("0")
            elif i == "l":
                ulang_list.append("1")
            elif i == " ":
                ulang_list.append(" ")

        binary_list = "".join(ulang_list).split()
        decimal_list = []

        for binary in binary_list:
            binary = "0b" + binary
            decimal_list.append(format(int(binary,2), "x"))

            print(decimal_list)"""

class pi:
    def __init__(self):
        f = open("data/pi.txt", "r")
        pi_data = f.readline()

        self.pi_data = pi_data

    def return_pi(self, index=3):
        return self.pi_data[:1 + index]
    
    def compare(self, user_input_pi):
        if user_input_pi == self.pi_data[:len(user_input_pi)]:
            return True, len(user_input_pi) 

        else:
            for i in range(len(self.pi_data[:len(user_input_pi)])):
                if self.pi_data[:len(user_input_pi)][i] == user_input_pi[i]:
                    pass
                else:
                    not_match_nu = i
                    break
            return False, not_match_nu