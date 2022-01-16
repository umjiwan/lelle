import discord
import asyncio
import os.path
import sys
from discord.ext import commands
from discord.ext.commands.converter import EmojiConverter
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

@client.command(aliases=["도움말"])
async def lelle_help(ctx, help_option):
    if help_option == "주식":
        embed = discord.Embed(color=0x99ddff)
        embed.set_author(name="lelle | stock", icon_url="https://raw.githubusercontent.com/umjiwan/lelle/main/img/lelle_ico.png")
        embed.add_field(name="소개", value="원하는 주식에 대한 정보를 알려드립니다.", inline=False)
        embed.add_field(name="사용법", value="`u주식 <종목명|종목코드>`")
        
        await ctx.channel.send(embed=embed)

    elif help_option == "유러":
        embed = discord.Embed(color=0x99ddff)
        embed.set_author(name="lelle | ulang", icon_url="https://raw.githubusercontent.com/umjiwan/lelle/main/img/lelle_ico.png")
        embed.add_field(name="소개", value="문장을 유러로 암호화 해주거나 유러를 원래의 문장으로 복호화 해줍니다.", inline=False)
        embed.add_field(name="사용법", value="`u유러 <암호화|복호화> <원하는 문장>`")

        await ctx.channel.send(embed=embed)

@lelle_help.error
async def lelle_help_error(ctx, error):
    embed = discord.Embed(color=0x99ddff)
    embed.set_author(name="lelle  |  help", icon_url="https://raw.githubusercontent.com/umjiwan/lelle/main/img/lelle_ico.png")
    embed.add_field(name="사용법", value="`u도움말 <명령어>`", inline=False)
    embed.add_field(name="명령어", value="`주식`, `유러`", inline=False)
    
    await ctx.channel.send(embed=embed)

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

@client.command(aliases=["유러"])
async def ul_language(ctx, u_option, sentence):
    ul_lang = lelle.ulang(sentence)
    if u_option == "암호화":
        result = ul_lang.encryption()

        embed = discord.Embed(title="ulang  |  Encryption", color=0x99ddff)
        embed.add_field(name="문장", value=sentence, inline=False)
        embed.add_field(name="유러 문장", value=result, inline=False)

        await ctx.channel.send(embed=embed)

    elif u_option == "복호화":
        pass
    else:
        pass


client.run(token)
