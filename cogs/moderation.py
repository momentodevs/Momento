import discord
import asyncio
from discord.ext import tasks, commands, menus

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        while True:
            await asyncio.sleep(10)
            with open("spam_detect.txt", "r+") as file:
                file.truncate(0)
    
    async def on_message(message):
        counter = 0
        with open("spam_detect.txt", "r") as file:
            for lines in file:
                if lines.strip("\n") == str(message.author.id):
                    couter+=1
            
            file.writelines(f"{str(message.author.id)}\n")
            if counter > 5:
                await message.guild.ban(message.author, reason="spam")
                await asyncio.sleep(1)
                await message.guild.unban(message.author)
                print("spam detected")
                
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

