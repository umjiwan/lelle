import discord
import asyncio
import os.path
import sys
from discord.ext import commands
import lelle

ing = discord.Activity(type=discord.ActivityType.listening ,name="u도움말")
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
    price = stock.price()
    compare = stock.compare()
    fluctuating = stock.fluctuating()
    sellask = stock.sellask()
    buyask = stock.buyask()
    transaction = stock.transaction()

    await ctx.channel.send(name)
    await ctx.channel.send(price)
    await ctx.channel.send(compare)
    await ctx.channel.send(fluctuating)
    await ctx.channel.send(sellask)
    await ctx.channel.send(buyask)
    await ctx.channel.send(transaction)

@stock.error
async def stock_error(ctx, error):
    await ctx.channel.send("주식 <종목명> 양식에 맞게 입력하여주세요.")


client.run(token)