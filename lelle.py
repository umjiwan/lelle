# maby ul

from os import lseek
from urllib import parse
from bs4 import BeautifulSoup
import requests
import re
import sqlite3
import datetime

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

class profile_word:
    def __init__(self, userid):
        conn = sqlite3.connect("data/lelle.db")
        cursor = conn.cursor()

        cursor.execute("CREATE TABLE IF NOT EXISTS word (\
                        userid text PRIMARY KEY, \
                        word text, \
                        writetime text)")

        conn.commit()
        conn.close()
        
        self.userid = userid
    
    def WriteWord(self, word):
        conn = sqlite3.connect("data/lelle.db")
        cursor = conn.cursor()
        cursor.execute(f"SELECT userid FROM word WHERE userid='{self.userid}'")
        result = cursor.fetchone()
        now = str(datetime.datetime.now())

        if result == None:
            cursor.execute(f"INSERT INTO word VALUES(\
                            '{self.userid}',\
                            '{word}',\
                            '{now}')")
        else:
            cursor.execute(f"UPDATE word SET word = '{word}' WHERE userid='{self.userid}'")
        
        conn.commit()
        conn.close()

    def DeleteWord(self):
        conn = sqlite3.connect("data/lelle.db")
        cursor = conn.cursor()

        cursor.execute(f"DELETE FROM word WHERE userid='{self.userid}'")
        
        conn.commit()
        conn.close()

    def ViewWord(self):
        conn = sqlite3.connect("data/lelle.db")
        cursor = conn.cursor()

        cursor.execute(f"SELECT word From word WHERE userid='{self.userid}'")
        word = cursor.fetchone()

        if word == None:
            return "한마디를 작성하시지 않으셨습니다."

        return word[0]

class Dday:
    def __init__(self, userid, day, honne=True):

        conn = sqlite3.connect("data/lelle.db")
        cursor = conn.cursor()

        cursor.execute("CREATE TABLE IF NOT EXISTS dday (\
                        userid text PRIMARY KEY, \
                        now text, \
                        day text)")

        conn.commit()
        conn.close()

        now = datetime.datetime.now()

        self.now = now
        self.day = day
        self.userid = userid
        self.honne = honne
       
    def SaveDday(self):
        conn = sqlite3.connect("data/lelle.db")
        cursor = conn.cursor()

        cursor.execute(f"SELECT day FROM dday WHERE userid='{self.userid}'")
        result = cursor.fetchone()

        conn.commit()
        conn.close

        if result == None:
            cursor.execute(f"INSERT INTO dday VALUES(\
                            '{self.userid}',\
                            '{self.now}',\
                            '{self.day}')")
        else:
            cursor.execute(f"UPDATE dday SET day = '{self.day}' WHERE userid='{self.userid}'")
        
        conn.commit()
        conn.close()
    
    def DeleteDday(self):
        conn = sqlite3.connect("data/lelle.db")
        cursor = conn.cursor()

        cursor.execute(f"DELETE FROM dday WHERE userid='{self.userid}'")
        
        conn.commit()
        conn.close()

    def ViewDday(self):
        conn = sqlite3.connect("data/lelle.db")
        cursor = conn.cursor()

        cursor.execute(f"SELECT now, day FROM dday WHERE userid='{self.userid}'")
        result = cursor.fetchone()
        
        conn.close()

        if result == None:
            return None

        day = result[1].split("-")
        day = datetime.datetime(int(day[0]), int(day[1]), int(day[2]))

        dday = str((self.now - day).days + self.honne)

        if dday[0] != "-":
            dday = "+" + dday

        return dday 
        

    

