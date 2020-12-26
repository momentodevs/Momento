import asyncio
import discord
from discord.ext import commands
import os
import toml
from pretty_help import PrettyHelp, Navigation

intents = discord.Intents.default()
intents.members = True

bot = commands.AutoShardedBot(command_prefix=commands.when_mentioned_or("m?"), description="Momento, A Multi-Purpose discord bot hosted 24/7", intents=intents)
 
with open("config.toml") as f:
    bot.config = toml.load(f)

nav = Navigation("\U000025c0\U0000fe0f", "\U000025b6\U0000fe0f")
color = discord.Color.blue()

bot.help_command = PrettyHelp(navigation=nav, color=color)


@bot.event
async def on_shard_ready(shard_id):
    print(f"Shard {shard_id} Ready!")

@bot.event 
async def on_ready():
    print(f"{bot.user} is ready")

TOKEN = bot.config["bot"]["token"]
bot.run(TOKEN)
