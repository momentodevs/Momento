import discord
from discord.ext import commands, menus, tasks
from db import db


class PlayerStatsTracker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = db

    @commands.Cog.listener()
    async def on_message(self, ctx):
        userId = ctx.author.id
        guildId = ctx.guild.id
        db.runCommand('userMessagesIncrement', userId, guildId)














def setup(bot):
    bot.add_cog(PlayerStatsTracker(bot))