import discord
from discord.embeds import Embed
from discord.ext import commands, menus, tasks
from discord.ext.commands.bot import AutoShardedBot
from discord.ext.commands.context import Context
from discord.member import Member
from discord.ext.commands import Cog
from discord import utils
from datetime import datetime
import math


class pcolours:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class PlayerStatsTracker(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.db = self.db

    @Cog.listener()
    async def on_message(self, ctx: Context):
        db = self.bot.db
        if ctx.webhook_id:
            pass
        else:
            userId = ctx.author.id
            guildId = ctx.guild.id
            user = self.bot.db.table('users').where(db.query().where('user_id', '=', userId).where('guild_id', '=', guildId)).first()
            print(user)

    @commands.command()
    @commands.guild_only()
    @commands.cooldown(rate=1, per=3, type=commands.BucketType.user)
    async def stats(self, ctx: Context, user: Member=None):
        """Check Stats for user, If no user mention it will default to command invoker"""
        db = self.bot.db
        if user is None:
            user = ctx.author
        userid = user.id
        guildid = ctx.guild.id
        response = await db.runCommand("getUserStats", userid, guildid)

        #page_1
        page_1 = Embed(title="User Stats", color=0x00ff59)
        page_1.set_author(name=user.display_name + user.discriminator, icon_url=user.avatar_url)
        page_1.add_field(name="Messages Sent", value=response[0], inline=False)
        page_1.add_field(name="Songs Played", value=response[1], inline=False)
        page_1.add_field(name="Join Date",
                        value=user.joined_at.strftime("%A, %d/%B/%Y at %H hours %M minutes %S seconds %Z"), inline=False)
        page_1.set_footer(text="Momento")
        await ctx.send(embed=page_1)

    #@stats.error
    #async def stats_handler(self, ctx: Context, error):
    #    if isinstance(error, commands.CommandOnCooldown):
    #        embed = discord.Embed(title="Cooldown!", colour=discord.Colour.red(),
    #                              description=f"Hold on there! Your typing too fast! Please retry in {math.floor(error.retry_after)} second")
    #
    #        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    #        embed.set_footer(text="Momento")
    #        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(PlayerStatsTracker(bot))
    print(pcolours.HEADER + "Loading Cog: Player Stats Tracker" + pcolours.ENDC)