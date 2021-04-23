import asyncio
import discord
from discord.ext import commands, ipc
import os
import toml
import datetime
import mysql.connector # from db import db (pfft.)
from pretty_help import PrettyHelp, DefaultMenu # 1.3.0 replaced navigation with DefaultMenu (might as well do so.) https://pypi.org/project/discord-pretty-help/ 
import logging
import sys
import os.path
from db import db

intents = discord.Intents.default()
intents.members = True
intents.presences = True


class Momento(commands.AutoShardedBot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ipc = ipc.Server(self, secret_key="5fnTUpsJ")

    async def on_ready(self):
        """Called upon the READY event"""
        print("Bot is ready.")

    async def on_ipc_ready(self):
        """Called upon the IPC Server being ready"""
        print("Ipc Server is ready.")

    async def on_ipc_error(self, endpoint, error):
        """Called upon an error being raised within the IPC route"""
        print(endpoint, "raised ", error)


bot = Momento(command_prefix=commands.when_mentioned_or("m?"), description="Momento, A Multi-Purpose discord bot hosted 24/7", intents=intents)
bot.launch_time = datetime.datetime.utcnow()


with open("config.toml") as f:
    bot.config = toml.load(f) # Load Config / Usable Globally

bot.load_extension('cogs.advanced_logs')
bot.load_extension('cogs.error_handler')
bot.load_extension('cogs.main')
#bot.load_extension('cogs.test-music')
#bot.load_extension('cogs.moderation')
#bot.load_extension('cogs.invite-tracker')
bot.load_extension('jishaku')
bot.load_extension('cogs.player-stats-tracker')

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

nav = DefaultMenu(page_left="\U000025c0\U0000fe0f", page_right="\U000025b6\U0000fe0f") # Left And Right Arrows For Help Navigation.
color = discord.Color.blue()

bot.help_command = PrettyHelp(navigation=nav, color=color) # Initiziation Of Help Command


@bot.event
async def on_shard_ready(shard_id):
    print(f"Shard {shard_id} Ready!")


@bot.ipc.route()
async def get_guild_count(data):
    return len(bot.guilds)


@bot.ipc.route()
async def get_guilds(data):
    return bot.guilds


@bot.ipc.route()
async def get_guild_ids(data):
    ids = []
    for i in bot.guilds:
        ids.append(i.id)
    return ids


TOKEN = bot.config["bot"]["token"] # Load Token
bot.ipc.start()
bot.run(TOKEN)
