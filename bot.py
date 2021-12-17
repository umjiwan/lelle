import discord
import asyncio
import os.path
import sys
from discord.ext import commands
import lelle

ing = discord.Activity(type=discord.ActivityType.listening, name="u도움말")
client = commands.Bot(status=discord.Status.online, activity=ing, command_prefix="u")

if os.path.isfile("token.txt"):
    pass
else:
    f = open("token.txt", "w")
    f.close()

f = open("token.txt", "r+")

if f.read() == "":
    print("Write token in the token.txt")
    f.close()
    sys.exit()
f.close()
    
f = open("token.txt", "r+")
token = str(f.read())
f.close()

@client.command(aliases=["주식"])
async def stock(ctx, *, s_name:str):
    stock = lelle.stock(s_name)
    name = stock.name()
    code = stock.code()
    price = stock.price()
    compare = stock.compare()
    pe_compare = stock.pe_compare()

    embed = discord.Embed(title=(f"{name}  |  {code}"), color=0x99ddff)
    embed.add_field(name="현재가", value=(f"{price}원"), inline=True)
    embed.add_field(name="등락율", value=pe_compare, inline=True)
    embed.add_field(name="전일대비", value=compare, inline=True)
    embed.set_footer(text=("Source by : "+ "https://finance.naver.com/item/main.naver?code=" + code))

    await ctx.channel.send(embed=embed)

@stock.error
async def stock_error(ctx, error):
    await ctx.channel.send("주식 <종목명> 양식에 맞게 입력하여주세요.")


client.run(token)