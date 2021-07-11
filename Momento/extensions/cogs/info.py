import psutil

from discord.ext import commands
from discord import Guild
from discord.ext.commands import Cog, AutoShardedBot, Context, BucketType
import discord

class Information(Cog):
    def __init__(self, bot: AutoShardedBot):
        """Main Commands"""
        self.bot = bot
        self.bot.db = self.db
        self.process = psutil.Process()

    @commands.command(name="info")
    async def test(self, ctx: Context):
        """Basic info About Momento"""
        await ctx.send(
            "<@734351336677834792> is a discord bot writen in Discord.py owned and maintained by <@734301865579380819>, <@616582088845688843> <a:wumpuscode:771579240184545310>")

    @commands.command(name="ping")
    async def ping(self, ctx: Context):
        """Bot Latency"""
        start = time.perf_counter()
        message = await ctx.send("Ping...")
        end = time.perf_counter()
        duration = (end - start) * 1000
        await message.edit(content='Pong! {:.2f}ms'.format(duration))

    @commands.guild_only()
    @commands.command(name="about")
    async def about(self, ctx: Context):
        '''Information about the bot'''
        # guild = ctx.message.channel.guild unused :(
        embed = discord.Embed(color=Colour.green())
        embed.title = 'Bot Info'
        embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
        try:
            embed.description = 'A multipurpose bot writen and maintained by TimmyTime#0310 and Mamoth112#8900\n[Support Server](https://discord.gg/SQzTAGzpT9)'
        except AttributeError:
            embed.description = 'A multipurpose bot writen and maintained by TimmyTime#0310 and Mamoth112#8900.\n[Support Server](https://discord.gg/SQzTAGzpT9)'
        embed.add_field(name="Servers", value=str(len(self.bot.guilds)))
        embed.add_field(name='Total Users', value=str(len(self.bot.users)))
        embed.add_field(name='Channels', value=f"{sum(1 for g in self.bot.guilds for _ in g.channels)}")
        embed.add_field(name="Library", value=f"discord.py")
        embed.add_field(name="Bot Latency", value=f"{round(self.bot.latency * 1000)}ms")
        embed.add_field(name="Invite",
                        value=f"[Click Here](https://discordapp.com/oauth2/authorize?client_id={self.bot.user.id}&scope=bot&permissions=268905542)")
        embed.set_footer(text="Momento © 2020 | Powered by discord.py")
        await ctx.send(embed=embed)

    @commands.command(aliases=['sinfo', 'guildinfo'])
    async def serverinfo(self, ctx: Context):
        """Server Information"""
        embed = discord.Embed(title="Server information",
                              colour=ctx.author.color,
                              timestamp=datetime.datetime.now())

        embed.set_thumbnail(url=ctx.guild.icon_url)

        statuses = [len(list(filter(lambda m: str(m.status) == "online", ctx.guild.members))),
                    len(list(filter(lambda m: str(m.status) == "idle", ctx.guild.members))),
                    len(list(filter(lambda m: str(m.status) == "dnd", ctx.guild.members))),
                    len(list(filter(lambda m: str(m.status) == "offline", ctx.guild.members)))]

        fields = [("ID", ctx.guild.id, False),
                  ("Owner", ctx.guild.owner, False),
                  ("Region", ctx.guild.region, False),
                  ("Created At", ctx.guild.created_at.strftime("%d/%m/%Y %H:%M:%S"), False),
                  ("Members", len(ctx.guild.members), False),
                  ("Humans", len(list(filter(lambda m: not m.bot, ctx.guild.members))), False),
                  ("Bots", len(list(filter(lambda m: m.bot, ctx.guild.members))), False),
                  ("Banned Members", len(await ctx.guild.bans()), False),
                  ("Statuses", f"🟢 {statuses[0]} 🟡 {statuses[1]} 🔴 {statuses[2]} ⚪ {statuses[3]}", False),
                  ("Text Channels", len(ctx.guild.text_channels), False),
                  ("Voice Channels", len(ctx.guild.voice_channels), False),
                  ("Categories", len(ctx.guild.categories), False),
                  ("Roles", len(ctx.guild.roles), False),
                  ("Invites", len(await ctx.guild.invites()), False),
                  ("\u200b", "\u200b", False)]

        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)

        await ctx.send(embed=embed)

    @commands.command()
    async def uptime(self, ctx: commands.Context):
        """: See how long I've been online"""
        time = datetime.now() - self.bot.starttime
        days = time.days
        hours, remainder = divmod(time.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        await ctx.channel.send(
            f"I've been online for {days} days, {minutes} min, {seconds} seconds!"
        )

    @commands.command(name="metrics", hidden=True)
    async def metrics(self, ctx: Context):
        '''Shows DB Stats'''
        db = self.bot.db
        await db.runCommand("getDatabaseStats", )

    @about.error
    async def clear_error(self, ctx: Context, error):
        if isinstance(error, CheckFailure):
            await ctx.send(f"<:redTick:596576672149667840> {error}")
        if isinstance(error, BadArgument):
            await ctx.send(f"<:redTick:596576672149667840> {error}")
        if isinstance(error, MissingRequiredArgument):
            await ctx.send(f"<:redTick:596576672149667840> {error}")
        raise error

    #@Cog.listener()
    #async def on_guild_join(self, guild: Guild):
    #    await db.runCommand('setGuildBase', guild.id)

    #@Cog.listener()
    #async def on_guild_leave(self, guild: Guild):
    #    await db.runCommand('removeGuild', guild.id)


def setup(bot):
    bot.add_cog(Information(bot))