import discord
from discord.ext import commands
from db import db
import time

class games(commands.Cog):
    def __init__(self, bot, *args, **kwargs):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        db.connect("./data/database.db")

    @commands.command()
    async def game(self, ctx, arg):

         if arg == "help":
            embed = discord.Embed(colour=0x9b59b6)
            embed.add_field(name="**Help with games**", value="A reference to all the commands and minigames.", inline=False)
            embed.set_footer(text="To suggest more minigames, dm 𝓣𝓲𝓶𝓶𝔂#6955")
            await ctx.reply(embed=embed, mention_author=False)

        elif arg == "count":
            embed = discord.Embed(colour=0x9b59b6)
            embed.add_field(name="**Count**", value="Count as high as you can!", inline=False)
            embed.set_footer(text="Winner gets 1000 coins!")
            await ctx.reply(embed=embed, mention_author=False)
        
        else:
            embed = discord.Embed(colour=0x9b59b6)
            embed.add_field(name="**Error :(**", value=f"Game: {arg} does not exist. Try running ***.game help*** for help  with game command...", inline=False)
            await ctx.reply(embed=embed, mention_author=False)

def setup(bot):
    bot.add_cog(games(bot))