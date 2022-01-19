from ast import alias
from dis import disco
from pydoc import cli
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
        embed.set_author(name="lelle | help", icon_url="https://raw.githubusercontent.com/umjiwan/lelle/main/data/img/lelle_ico.png")
        embed.add_field(name="소개", value="원하는 주식에 대한 정보를 알려드립니다.", inline=False)
        embed.add_field(name="사용법", value="`u주식 <종목명|종목코드>`")
        
        await ctx.channel.send(embed=embed)

    elif help_option == "유러":
        embed = discord.Embed(color=0x99ddff)
        embed.set_author(name="lelle | help", icon_url="https://raw.githubusercontent.com/umjiwan/lelle/main/data/img/lelle_ico.png")
        embed.add_field(name="소개", value="문장을 유러로 암호화 해주거나 유러를 원래의 문장으로 복호화 해줍니다.", inline=False)
        embed.add_field(name="사용법", value="`u유러 <암호화|복호화> <원하는 문장>`")

        await ctx.channel.send(embed=embed)

    elif help_option == "원주율" or help_option == "파이":
        embed = discord.Embed(color=0x99ddff)
        embed.set_author(name="lelle | help", icon_url="https://raw.githubusercontent.com/umjiwan/lelle/main/data/img/lelle_ico.png")
        embed.add_field(name="소개", value="원주율을 보거나 외울 수 있습니다.", inline=False)
        embed.add_field(name="사용법", value="`u<원주율|파이>`: 원주율을 보여줍니다 (900자리 까지)\n`u<원주율|파이> <원주율>`: 입력한 원주율 값을 검토해 만약 틀렸다면 틀린 부분을 알려줍니다.")

        await ctx.channel.send(embed=embed)

    elif help_option == "핑":
        embed = discord.Embed(color=0x99ddff)
        embed.set_author(name="lelle | help", icon_url="https://raw.githubusercontent.com/umjiwan/lelle/main/data/img/lelle_ico.png")
        embed.add_field(name="소개", value="봇의 핑 즉 레이턴시(지연시간) 을 출력해준다.", inline=False)
        embed.add_field(name="사용법", value="`u핑`")

        await ctx.channel.send(embed=embed)

@lelle_help.error
async def lelle_help_error(ctx, error):
    embed = discord.Embed(color=0x99ddff)
    embed.set_author(name="lelle  |  help", icon_url="https://raw.githubusercontent.com/umjiwan/lelle/main/data/img/lelle_ico.png")
    embed.add_field(name="사용법", value="`u도움말 <명령어>`", inline=False)
    embed.add_field(name="명령어", value="`주식`, `유러`, `원주율`, `핑`", inline=False)
    
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
        embed = discord.Embed(title="ulang  |  Decryption", color=0x99ddff)
        embed.add_field(name="공지", value="복호화 기능은 개발중입니다. 😢", inline=False)

    else:
        pass

@client.command(aliases=["원주율", "파이"])
async def pi(ctx, user_input_pi):
    class_pi = lelle.pi()
    compare, index = class_pi.compare(user_input_pi)
    
    if compare:
        title_sentence = ["맞았습니다!", "까지 외우셨습니다."]
    else:
        title_sentence = ["틀렸습니다!", "부터 틀리셨습니다."]
    
    embed = discord.Embed(color=0x99ddff)

    embed.set_author(name="lelle  |  pi", icon_url="https://raw.githubusercontent.com/umjiwan/lelle/main/data/img/lelle_ico.png")
    embed.add_field(name=title_sentence[0], value=f"{index}자리{title_sentence[1]}", inline=False)

    await ctx.channel.send(embed=embed)

@pi.error
async def pi_error(ctx, error):
    class_pi = lelle.pi()
    data_pi = class_pi.return_pi(index=900)

    embed = discord.Embed(color=0x99ddff)
    
    embed.set_author(name="lelle  |  pi", icon_url="https://raw.githubusercontent.com/umjiwan/lelle/main/data/img/lelle_ico.png")
    embed.add_field(name="원주율", value=data_pi, inline=False)

    await ctx.channel.send(embed=embed)

@client.command(aliases=["핑"])
async def ul_ping(ctx):
    embed = discord.Embed(color=0x99ddff)
    embed.add_field(name="pong! 🏓", value=f"`{int(client.latency*1000)}`ms", inline=False)

    await ctx.channel.send(embed=embed)

@client.command(aliases=["한마디"])
async def one_word(ctx, *, word):
    userid = ctx.author.id    
    pw = lelle.profile_word(userid)
    pw.WriteWord(word)

    await ctx.channel.send(f"한마디가 등록 되었습니다!")

@one_word.error
async def one_word_error(ctx, error):
    await ctx.channel.send(f"양식에 맞게 입력해주세요.")

@client.command(aliases=["프로필"])
async def user_profile(ctx):
    userid = ctx.author.id
    username = ctx.author.display_name
    userprofileimg = ctx.author.avatar_url
    usertag = ctx.author.mention

    pw = lelle.profile_word(userid)
    userword = pw.ViewWord()
    
    await ctx.channel.send(f"{usertag}님의 프로필")

    embed = discord.Embed(color=0x99ddff)

    embed.set_author(name="lelle  |  profile", icon_url="https://raw.githubusercontent.com/umjiwan/lelle/main/data/img/lelle_ico.png")
    embed.add_field(name="닉네임", value=username, inline=False)
    embed.add_field(name="한마디", value=userword, inline=False)
    embed.thumbnail(url=userprofileimg)

    await ctx.channel.send(embed=embed)

client.run(token)
