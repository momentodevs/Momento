import discord
from discord.ext import commands
import asyncio
import asyncpg
import time
import os

class Level(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        credentials = {"user": "USERNAME", "password": "PASSWORD", "database": "DATABSE", "host": "127.0.0.1"}
         try:
             await bot.start(config.token)
         except KeyboardInterrupt:
             await db.close()
             await bot.logout()


def setup(client):
    bot.add_cog(Level(bot))
