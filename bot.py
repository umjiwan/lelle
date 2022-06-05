from discord.ext import commands
import discord
from lelle import stock
import os

lelle = commands.Bot(
    command_prefix="t",
    status=discord.Status.online,

    activity=discord.Activity(
        type=discord.ActivityType.listening,
        name="u도움말")
)

@lelle.event
async def on_ready():
    print("-" * 10)
    print(f"name: {lelle.user.name}")
    print(f"id: {lelle.user.id}")
    print("-" * 10)

# 명령 파일 가져오기
for file in os.listdir("lelle/"):
    if file[-3:] == ".py":
        lelle.load_extension(f"lelle.{file[:-3]}")

with open("data/token.txt", "r") as token_file:
    token = token_file.read()

lelle.run(token)