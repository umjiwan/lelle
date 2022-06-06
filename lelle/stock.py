from lib2to3.pytree import convert
from urllib import parse
from bs4 import BeautifulSoup
import requests
import discord
from discord.ext import commands

class url:
    def __init__(self, stock: str):
        self.stock = stock
        self.BASE_URL = "https://finance.naver.com"

    def convert_stock(self):
        return parse.quote(self.stock.encode("euc-kr"))

    def get(self):
        search_url = self.BASE_URL + "/search/searchList.naver?query=" + self.convert_stock()
        search_response = requests.get(search_url)
        search_html = search_response.text
        search_soup = BeautifulSoup(search_html, "html.parser")
        search_selector = "#content > div.section_search > table > tbody > tr:nth-child(1) > td.tit > a"

        return self.BASE_URL + str(search_soup.select_one(search_selector).get("href"))

class data:
    def __init__(self, stock: str):
        self.url = url(stock).get()
        self.response = requests.get(self.url)
        self.html = self.response.text
        self.soup = BeautifulSoup(self.html, "html.parser")

    def get_name(self):
        selector = "#middle > div.h_company > div.wrap_company > h2 > a"
        return self.soup.select_one(selector).text

    def get_code(self):
        selector = "#middle > div.h_company > div.wrap_company > div > span.code"
        return self.soup.select_one(selector).text

    def get_price(self, convert: bool=False):
        selector = "#chart_area > div.rate_info > div > p > em > span.blind"
        price = self.soup.select_one(selector).text

        return price if not convert else int(price.replace(",", ""))

    def get_yesterday_price(self, convert: bool=False):
        selector = "#chart_area > div.rate_info > table > tr > td.first > em > span.blind"
        yesterday_price = self.soup.select_one(selector).text

        return yesterday_price if not convert else int(yesterday_price.replace(",", ""))

    def get_change(self, percent: bool=False):
        price = self.get_price(convert=True)
        yesterday_price = self.get_yesterday_price(convert=True)
        compare = price - yesterday_price

        return compare if not percent else round(compare / yesterday_price * 100, 2)

class Core(commands.Cog):
    def __init__(self, lelle):
        self.lelle = lelle
    
    @commands.command(aliases=["주식"])
    async def stock(self, ctx, stock_name: str):
        stock = data(stock_name)

        embed = discord.Embed(
            title=f"{stock.get_name()} | {stock.get_code()}",
            color=0x99ddff
        )

        embed.add_field(
            name="현재가",
            value=stock.get_price(),
            inline=True
        )

        price_is_up = True if stock.get_change() >= 0 else False

        embed.add_field(
            name="등락율",
            value=f'{"+" if price_is_up else ""}' + f"{stock.get_change(percent=True)}" + "%",
            inline=True
        )

        embed.add_field(
            name="전일대비",
            value=f'{"+" if price_is_up else ""}' + stock.get_change(),
            inline=True
        )

        embed.set_footer(text="원하시는 결과가 아닌가요? <종목코드> 로 검색해보세요.")

        await ctx.channel.send(embed=embed)
       
def setup(lelle):
    lelle.add_cog(Core(lelle))

if __name__ == "__main__":
    stock = data("kakao")
    print(stock.get_name())
    print(stock.get_price())
    print(stock.get_yesterday_price())
    print(stock.get_change())
    print(stock.get_change(percent=True))