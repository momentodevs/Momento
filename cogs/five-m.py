import discord
from discord.ext import commands, menus, tasks
from fivem import FiveM

class FiveM(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

