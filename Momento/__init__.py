import sys
import time
from pathlib import Path
from datetime import datetime

import discord
import jthon
import yaml
from aiohttp import ClientSession
from discord.ext import commands
from orator import DatabaseManager

from Momento.utils import MakeSettings
from Momento.utils.basic_bot import BasicBot

# Check the installed python version
if sys.version_info <= (3, 6):
    print("Need Python 3.6 or greater to run this bot. Exiting...")
    time.sleep(3)
    sys.exit()


__version__ = "0.1.1"

# Basic invite link for your bot. Specify more permissions on the discord.app site
invite_link = "https://discordapp.com/api/oauth2/authorize?client_id={}&scope=bot&permissions=8"

# Get the bot settings or create them if they arenot already made
settings = MakeSettings(settings="./Momento/database/json/").get_settings()

# Load the config file
with open("config.yaml") as file:
    config = yaml.safe_load(file)
intents = discord.Intents.default()
intents.members = True
intents.presences = True
# Create a discord bot instance
initial = settings.data.get("Bot Settings")
bot = BasicBot(
    intents=intents,
    **initial,
    db=DatabaseManager(config.get("databases")),
    settings=settings,
)
bot.remove_command('help')

# Basic message to console when the bot is ready
@bot.event
async def on_ready():
    print(f"Logged in as: {bot.user.name}")
    print(f"With user ID: {bot.user.id}")
    print(f"Invite Link: {invite_link.format(bot.user.id)}\n")


# pull all potential extensions from the extensions folder
def collect_extensions():
    files = Path("Momento", "extensions").rglob("*.py")
    for file in files:
        if "__init__" not in file.name:
            yield file.as_posix()[:-3].replace("/", ".")


# load cogs and commands from the bot.extensions folder
async def load_extensions():
    await bot.load_extension('jishaku')
    for extension in collect_extensions():
        try:
            await bot.load_extension(extension)
            print(f"Loaded {extension}")
        except Exception as e:
            print(f"Failed to load extension {extension}\n{e}")
    print()


async def run():
    # Load bot utilities if enabled in the config
    utils = config.get("config", {}).get("utils", {})
    from .utils import Bot_Logging, Bot_Settings, Bot_Utils

    if utils.get("bot_logging", True):
        await bot.add_cog(Bot_Logging.Bot_Logging(bot))
    if utils.get("bot_settings", True):
        await bot.add_cog(Bot_Settings.Bot_Settings(bot))
    if utils.get("bot_utils", True):
        await bot.add_cog(Bot_Utils.Bot_Utils(bot))

    await load_extensions()

    # Run the bot
    await bot.run(config.get("discord").get("TOKEN"))