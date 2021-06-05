from datetime import datetime

from discord.ext import commands

from . import checks
from .. import collect_extensions


class Bot_Utils(commands.Cog):
    """Some useful utils for the discord bot"""

    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.bot.starttime = datetime.now()

    @checks.is_owner_or_coowner()
    @commands.command()
    async def extensions(self, ctx: commands.Context):
        """
        : Get a list of currently loaded and unloaded extensions. The names can be used for the load/unload/reload commands
        """
        loaded = "\n".join(iter(self.bot.extensions))
        unloaded = "\n".join(
            extension
            for extension in collect_extensions()
            if extension not in self.bot.extensions
        )

        await ctx.send(f"```Loaded:\n\n{loaded}\n\nUnloaded:\n\n{unloaded}```")

    @checks.is_owner_or_coowner()
    @commands.command()
    async def shutdown(self, ctx: commands.Context):
        """: Shutdown the bot"""
        await ctx.channel.send("Shutting Down!")
        self.bot.reboot = False
        await self.bot.logout()
        await self.bot.close()

    # unload an extension
    @checks.is_owner_or_coowner()
    @commands.command()
    async def unload(self, ctx: commands.Context, extension: str = None):
        """: Unload an extension"""
        try:
            self.bot.unload_extension(extension)
            await ctx.channel.send(f"Unloaded Extension: {extension}")
        except:
            await ctx.channel.send("unable to unload extenstion!")

    # load an extension
    @checks.is_owner_or_coowner()
    @commands.command()
    async def load(self, ctx: commands.Context, extension: str = None):
        """: Load an extension"""
        try:
            self.bot.load_extension(extension)
            await ctx.channel.send(f"Loaded Extension: {extension}")
        except:
            await ctx.channel.send("Unable to load extenstion!")

    # reload an extension
    @checks.is_owner_or_coowner()
    @commands.command(name="reload")
    async def _reload(self, ctx: commands.Context, extension: str = None):
        """: Reload an extension"""
        try:
            self.bot.reload_extension(extension)
            await ctx.channel.send(f"Reloaded Extension: {extension}")
        except:
            await ctx.channel.send("Unable to reload extension!")