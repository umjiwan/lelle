import discord
import asyncio
import os.path
import sys
import lelle


client = discord.Client()

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

@client.event
async def on_ready():
    print("login!")
    print(client.user.name)
    print(client.user.id)
    print("-"*15)

@client.event
async def on_message(message):
    if message.author.bot:
        return None
    if message.content.startswith("u"):
        msg = message.content[1:]
    else:
        return None


    if msg[:2] == "주식":
        stock = lelle.stock(msg[3:])
        name = stock.name()
        price = stock.price()
        compare = stock.compare()
        fluctuating = stock.fluctuating()
        sellask = stock.sellask()
        buyask = stock.buyask()
        transaction = stock.transaction()

        await message.channel.send(name)
        await message.channel.send(price)
        await message.channel.send(compare)
        await message.channel.send(fluctuating)
        await message.channel.send(sellask)
        await message.channel.send(buyask)
        await message.channel.send(transaction)

client.run(token)