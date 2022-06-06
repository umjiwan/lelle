import discord
from discord.ext import commands

class Core(commands.Cog):
    def __init__(self, lelle):
        self.lelle = lelle

    @commands.command(aliases=["도움말"])
    async def _help(self, ctx, command: str=None):
        await ctx.channel.send(command)

def setup(lelle):
    lelle.add_cog(Core(lelle))