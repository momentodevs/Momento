import asyncio
import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.members = True

bot = commands.AutoShardedBot(command_prefix=commands.when_mentioned_or("test|"), description="Momento, A Multi-Purpose discord bot hosted 24/7")

bot.load_extension('jishaku')
bot.load_extension('cogs.main')


@bot.event
async def on_shard_ready(shard_id):
    print(f"Shard {shard_id} Ready!")

@bot.event 
async def on_ready():
    print(f"{bot.user} is ready")
    bot.loop = asyncio.get_event_loop







TOKEN = os.environ['BOT_TOKEN']
bot.run(TOKEN)