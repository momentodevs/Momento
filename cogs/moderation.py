import discord
import asyncio
from discord.ext import tasks, commands, menus

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    @commands.guild_only()
    @commands.bot_has_permissions(manage_messages=True)
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int = 1):
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"<:greenTick:596576670815879169> {amount} messages have been just deleted")
        await asyncio.sleep(2)
        await ctx.channel.purge(limit=1)

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send(f"<:redTick:596576672149667840> {error}")
        if isinstance(error, commands.BadArgument):
            await ctx.send(f"<:redTick:596576672149667840> {error}")
        raise error


    #@commands.command()
    #@commands.guild_only()
    #@commands.bot_has_permissions(manage_messages=True)
    #async def 

def setup(bot):
    bot.add_cog(Moderation(bot))

