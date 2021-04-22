import discord
import requests
import json
from discord.ext import commands
from pycoingecko import CoinGeckoAPI # https://pypi.org/project/pycoingecko/ (docs and installation)
cg = CoinGeckoAPI()

class Crypto(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def crypto(self, ctx, coin):
        price = cg.get_price(ids=coin, vs_currencies='usd')
        price_frmat = price[coin]['usd']
        await ctx.send(f"1 ${coin.upper()} is equal to {price_frmat:,.2f}$")

def setup(bot):
    bot.add_cog(Crypto(bot))
