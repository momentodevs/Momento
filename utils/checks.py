"""
A list of checks to use for the bot.
Example:
Transforming common checks into its own decorator:
    .. code-block:: python
        def is_me():
            def predicate(ctx):
                return ctx.author.id == 'my-user-id'
            return commands.check(predicate)
        @bot.command()
        @is_me()
        async def only_me():
            await bot.say('Only you!')
"""

import discord
from discord.ext import commands


def is_owner_or_coowner():
    "Checks if the user is the bot owner or a coowner"

    async def predicate(ctx):
        coowners = ctx.bot.settings.data.get("coowners", [])
        bot = await ctx.bot.application_info()
        if ctx.author.id in coowners:
            return True
        if ctx.author == bot.owner:
            return True

    return commands.check(predicate)


def is_guild_owner():
    """Checks if the message author is the guild owner"""

    def predicate(ctx):
        if not ctx.guild:
            return False
        return ctx.author is ctx.guild.owner

    return commands.check(predicate)