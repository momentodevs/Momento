import discord
from discord.ext import commands, menus, tasks


class API(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



def setup(bot):
    bot.add_cog(API(bot))