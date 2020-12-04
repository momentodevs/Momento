import discord
import psutil
import time
from discord.ext import commands


class Main(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.process = psutil.Process()
    
    
    @commands.command(name="info")
    async def test(self, ctx):
        await ctx.send("<@734351336677834792> is a discord bot writen in Discord.py owned and maintained by <@734301865579380819> :wumpuscode:")


    @commands.command(name="ping")
    async def ping(self, ctx):
        """Shows Message Edit Latency Between The Bot And Discord Servers"""
        start = time.perf_counter()
        message = await ctx.send("Ping...")
        end = time.perf_counter()
        duration = (end - start) * 1000
        await message.edit(content='Pong! {:.2f}ms'.format(duration))
        

def setup(bot):
    bot.add_cog(Main(bot))