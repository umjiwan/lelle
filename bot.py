import discord
import asyncio
import os.path
import sys

client = discord.Client()

"""if os.path.isfile("token.txt"):
    pass
else:
    f = open("token.txt", "w")
    f.close()

f = open("token.txt", "r+")

if f.read() == "":
    print("Write token in the token.txt")
    sys.exit()

token = f.read()
print(f.read())
f.close()"""

token = "OTIwNjEzOTI4MjAyMDE4ODk5.Ybm6iA.EIQlXpVHb7osvgBg95Qgz4tgWlc"
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
    if message.content == "ping":
        await message.channel.send("pong")

client.run(token)