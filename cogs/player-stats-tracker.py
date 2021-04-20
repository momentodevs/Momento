import discord
from discord.ext import commands, menus, tasks

class PlayerStatsTracker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot













def setup(bot):
    bot.add_cog(PlayerStatsTracker(bot))