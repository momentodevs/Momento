import discord
from discord.ext import commands
import re
from . import checks
from .Bot_Logging import human


class Bot_Settings(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot

    @checks.is_owner_or_coowner()
    @commands.command(aliases=["sp"])
    async def set_prefix(self, ctx: commands.Context, *, prefix: str = "!"):
        """: Change the prefix for using bot commands. This will overwrite all prefixes."""
        self.cleanStr(prefix)
        prefix = prefix.split(" ")
        self.bot.command_prefix = prefix
        self.bot.settings.data["Bot Settings"]["command_prefix"] = prefix
        self.bot.settings.save()
        await ctx.channel.send(
            f'Commands will now be called with **{", ".join(prefix)}**'
        )

    @checks.is_owner_or_coowner()
    @commands.command(name="toggle_traceback")
    async def _print_traceback(self, ctx: commands.Context):
        """: Toggle printing the traceback for debugging"""
        self.bot.settings.data["traceback"] = not self.bot.settings.data["traceback"]
        self.bot.settings.save()
        await ctx.channel.send(
            f'Traceback is now: {human.get(self.bot.settings.data.get("traceback"))}'
        )

    @checks.is_owner_or_coowner()
    @commands.command()
    async def change_description(self, ctx: commands.Context, *, description: str = ""):
        """: Change the description for the bot displayed in the help menu"""
        self.cleanStr(description)
        self.bot.description = description
        self.bot.settings.data["Bot Settings"]["description"] = description
        self.bot.settings.save()
        await ctx.channel.send(f"The bots description is now ```{description}```")

    @checks.is_owner_or_coowner()
    @commands.command()
    async def toggle_help(self, ctx: commands.Context):
        """: Toggle how the bot send the help menu in a pm"""
        dm_help = not self.bot.help_command.dm_help
        self.bot.help_command = commands.DefaultHelpCommand(dm_help=dm_help)
        self.bot.settings.data["Bot Settings"]["pm_help"] = dm_help
        self.bot.settings.save()
        if dm_help:
            await ctx.channel.send("The help menu will be sent as a PM now.")
        else:
            await ctx.channel.send("The help menu will be posted locally.")

    @checks.is_owner_or_coowner()
    @commands.command()
    async def add_coowner(self, ctx: commands.Context, member: discord.Member = None):
        """: Add a co-owner to your bot
        WARNING!! A coowner can use the same commands as the owner!"""
        if member is None:
            return
        else:
            config = self.bot.settings
            if "coowners" not in config.data:
                config.data["coowners"] = []
            if member.id not in config.data["coowners"]:
                config.data["coowners"].append(member.id)
                config.save()
                await ctx.channel.send(
                    f"{member.mention} has been added as a co-owner!"
                )

    @checks.is_owner_or_coowner()
    @commands.command()
    async def remove_coowner(
        self, ctx: commands.Context, member: discord.Member = None
    ):
        ": Remove a co-owner from your bot"
        if member is None:
            return
        else:
            config = self.bot.settings
            if "coowners" not in config.data:
                config.data["coowners"] = []
            if member.id in config.data["coowners"]:
                config.data["coowners"].remove(member.id)
                config.save()
                await ctx.channel.send(
                    f"{member.mention} has been removed from co-owners!"
                )

    @checks.is_owner_or_coowner()
    @commands.command()
    async def coowners(self, ctx: commands.Context):
        ": Check the co-owners of a bot"
        coowners = ""
        for coowner in self.bot.settings.data.get("coowners", []):
            coowners += f"{ctx.bot.get_user(coowner)}\n"
        embed = discord.Embed(title="Co-Owners", description=coowners)
        await ctx.channel.send(embed=embed)

    async def cleanStr(text: str):
        # Returns a string clean of non-utf8 characters and quote marks (" and ')
        text = text.decode("utf8","ignore") 
        text = text.replace("'", "") 
        text = text.replace('"', "")
        return text