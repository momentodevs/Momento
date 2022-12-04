import asyncio
import discord
from discord.ext import commands
import os
import toml
import mysql.connector # from db import db (pfft.)
from pretty_help import PrettyHelp, EmojiMenu # 1.3.0 replaced navigation with DefaultMenu (might as well do so.) https://pypi.org/project/discord-pretty-help/ 

intents = discord.Intents.default()
intents.members = True
intents.presences = True

bot = commands.AutoShardedBot(command_prefix=commands.when_mentioned_or("m?"), description="Momento, A Multi-Purpose discord bot hosted 24/7", intents=intents)

with open("config.toml") as f:
    bot.config = toml.load(f) # Load Config / Usable Globally

bot.load_extension('jishaku')
bot.load_extension('cogs.main')
bot.load_extension('cogs.test-music')
bot.load_extension('cogs.moderation')
bot.load_extension('cogs.invite-tracker')
bot.load_extension('cogs.crypto')
import logging

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

nav = EmojiMenu(page_left="\U000025c0\U0000fe0f", page_right="\U000025b6\U0000fe0f", remove=":discord:743511195197374563") # Left And Right Arrows For Help Navigation.
ending_note = "The ending note from {ctx.bot.user.name}\nFor command {help.clean_prefix}{help.invoked_with}"

bot.help_command = PrettyHelp(menu=nav, ending_note=ending_note) # Initiziation Of Help Command

@bot.event
async def on_shard_ready(shard_id):
    print(f"Shard {shard_id} Ready!")

@bot.event
async def on_ready():
    print(f"{bot.user} is ready")

TOKEN = bot.config["bot"]["token"] # Load Token
bot.run(TOKEN)
