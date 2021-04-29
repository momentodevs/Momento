import logging
import traceback
from pathlib import Path

import discord
import jthon
from discord.ext import commands

from .. import config
from . import checks, query_logger

path = Path("Momento", "database", "json", "log_settings.json")
file = jthon.load(path.as_posix())
if not path.is_file():
    file.data = {
        "log_level": logging.INFO,
        "log_error": False,
        "log_message": False,
        "log_message_edit": False,
        "log_command": False,
        "log_command_error": False,
        "traceback": False,
    }
    file.save()

LOGS = logging.getLogger("discord")
LOGS.setLevel(logging.INFO)
HANDLER = logging.FileHandler(
    filename="discord.log",
    encoding="utf-8",
    mode=config.get("config").get("logging_mode", "w"),
)
HANDLER.setFormatter(
    logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
)
LOGS.addHandler(HANDLER)


def guild_check(guild):
    if not guild:
        return "DM Channel"
    return guild.id


async def log_error(error, event, *args, **kwargs):

    if file.get("traceback"):
        tb = kwargs.get("tb")
        if tb:
            print(tb)
    else:
        print(error)
    LOGS = logging.getLogger(f"discord.{event}.error")
    LOGS.warning("Event: {} Error: {}".format(event, error))


human = {True: "on", False: "off"}


class Bot_Logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.add_check(self.log_command)
        self.bot.logging = file
        LOGS.setLevel(self.bot.logging.data["log_level"])

    @commands.Cog.listener()
    async def on_message(self, message):
        if (
            self.bot.logging.data["log_message"]
            and message.author.id != self.bot.user.id
        ):
            LOGS = logging.getLogger("discord.message")
            LOGS.info(
                f"Server_id: {guild_check(message.guild)} "
                f"Author_id: {message.author.id} "
                f"Message: {message.content}"
            )

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if (
            self.bot.logging.data["log_message_edit"]
            and before.author.id != self.bot.user.id
        ):
            LOGS = logging.getLogger("discord.message.edit")
            LOGS.info(
                f"Server_id: {guild_check(before.guild)} "
                f"Author_id: {before.author.id} "
                f"Original: {before.content} "
                f"Edited: {after.content}"
            )

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
        if self.bot.settings.data.get("traceback"):
            await commands.bot.BotBase(self.bot).on_command_error(ctx, error)
        else:
            print(error)
        if self.bot.logging.data["log_command_error"]:
            LOGS = logging.getLogger("discord.command.error")
            LOGS.warning(
                f"Server_id: {guild_check(ctx.message.guild)} "
                f"Author_id: {ctx.message.author.id} "
                f"Command: {ctx.invoked_with} "
                f"Error: {error} "
            )

    def log_command(self, ctx: commands.Context):
        if self.bot.logging.data["log_command"]:
            LOGS = logging.getLogger("discord.command")
            LOGS.info(
                f"Server_id: {guild_check(ctx.message.guild)} "
                f"Author_id: {ctx.message.author.id} "
                f"Command: {ctx.invoked_with}"
            )
        return True

    @checks.is_owner_or_coowner()
    @commands.group(pass_context=True)
    async def toggle_log(self, ctx: commands.Context):
        """: Toggle what the bot will log"""
        if not ctx.invoked_subcommand:
            await ctx.channel.send("No/Invalid toggle")

    @toggle_log.command(name="message")
    async def _message(self, ctx: commands.Context):
        """: Log Messages"""
        await self.log_toggler(ctx, "log_message", "Message")

    @toggle_log.command(name="message_edit")
    async def _message_edit(self, ctx: commands.Context):
        """: Log Edited Messages"""
        await self.log_toggler(ctx, "log_message_edit", "Message Edit")

    @toggle_log.command(name="error")
    async def _error(self, ctx: commands.Context):
        """: Log Errors"""
        await self.log_toggler(ctx, "log_error", "Error")

    @toggle_log.command(name="command")
    async def _command(self, ctx: commands.Context):
        """: Log Commands used"""
        await self.log_toggler(ctx, "log_command", "Command")

    @toggle_log.command(name="command_error")
    async def _command_error(self, ctx: commands.Context):
        """: Log Errors from Commands"""
        await self.log_toggler(ctx, "log_command_error", "Command Error")

    @toggle_log.command(name="level")
    async def _log_level(self, ctx: commands.Context, level: str = None):
        """: Set the logging level (Default Level: INFO)"""
        levelname = level.upper()
        level = logging._nameToLevel.get(levelname)
        if level is None:
            await ctx.channel.send("Invalid Level")
        else:
            self.bot.logging.data["log_level"] = level
            self.bot.logging.save()
            LOGS.setLevel(self.bot.logging.data["log_level"])
            await ctx.channel.send(f"Log Level is now: {levelname}")

    async def log_toggler(self, ctx: commands.Context, log_type, generic_name):
        state = not self.bot.logging.data[log_type]
        self.bot.logging.data[log_type] = state
        self.bot.logging.save()
        if log_type == "traceback":
            await ctx.channel.send(f"{generic_name} is now: {human[state]}")
        else:
            await ctx.channel.send(f"{generic_name} logging is now: {human[state]}")