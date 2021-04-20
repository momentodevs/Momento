import discord
import psutil
import time
from discord.ext import commands



class Information(commands.Cog):
    def __init__(self, bot):
        """Main Commands"""
        self.bot = bot
        self.process = psutil.Process()
    
    
    @commands.command(name="info")
    async def test(self, ctx):
        await ctx.send("<@734351336677834792> is a discord bot writen in Discord.py owned and maintained by <@734301865579380819> <a:wumpuscode:771579240184545310>")


    @commands.command(name="ping")
    async def ping(self, ctx):
        """Bot Latency"""
        start = time.perf_counter()
        message = await ctx.send("Ping...")
        end = time.perf_counter()
        duration = (end - start) * 1000
        await message.edit(content='Pong! {:.2f}ms'.format(duration))

    @commands.guild_only()
    @commands.command(name="about")
    async def about(self, ctx):
        '''Information about the bot'''
        # guild = ctx.message.channel.guild unused :(
        embed = discord.Embed(color=discord.Color.green())
        embed.title = 'Bot Info'
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        try:
            embed.description = 'A multipurpose bot writen and maintained by TimmyTime#0310\n[Support Server](https://discord.gg/SQzTAGzpT9)'
        except AttributeError:
            embed.description = 'A multipurpose bot writen and maintained by TimmyTime#0310.\n[Support Server](https://discord.gg/SQzTAGzpT9)'
        embed.add_field(name="Servers", value=len(self.bot.guilds))
        embed.add_field(name='Total Users', value=len(self.bot.users))
        embed.add_field(name='Channels', value=f"{sum(1 for g in self.bot.guilds for _ in g.channels)}")
        embed.add_field(name="Library", value=f"discord.py")
        embed.add_field(name="Bot Latency", value=f"{round(self.bot.latency * 1000)}ms")
        embed.add_field(name="Invite", value=f"[Click Here](https://discordapp.com/oauth2/authorize?client_id={self.bot.user.id}&scope=bot&permissions=268905542)")
        embed.set_footer(text="Momento © 2020 | Powered by discord.py")
        await ctx.send(embed=embed)


    @about.error
    async def clear_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send(f"<:redTick:596576672149667840> {error}")
        if isinstance(error, commands.BadArgument):
            await ctx.send(f"<:redTick:596576672149667840> {error}")
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"<:redTick:596576672149667840> {error}")
        raise error

            
def setup(bot):
    bot.add_cog(Information(bot))