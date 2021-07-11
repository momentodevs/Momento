import discord
from discord.ext import commands
from discord.ext.commands import Context
from discord import TextChannel, Colour, Member, User
from discord.ext.commands.bot import AutoShardedBot
from discord.ext.commands.cog import Cog
from discord.utils import get
from db import db
import datetime



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


class Welcomer(Cog):
    def __init__(self, bot: AutoShardedBot):
        self.bot = bot
        self.db = self.bot.db

    @commands.command()
    @commands.guild_only()
    async def welcomeMessage(self, ctx: Context, value):
        """Command to modify the settings of the welcome Messages, Must Pass the name of the config to change and the value"""
        guildId = ctx.guild.id
        await ctx.send("Welcome Message can use {user_name}, {user_discriminator}, {guild_name}, {user_mention}")
        welcomeMessage = await db.runCommand('getGuildWelcomeMessage', guildId)
        await self.db.runCommand('setGuildWelcomeMessage', guildId, value)
        embed = discord.Embed(title="Welcomer Settings", colour=discord.Colour(0x1e240),
                              timestamp=datetime.datetime.utcnow())
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.set_author(name=ctx.author.display_name+"#"+ctx.author.discriminator, icon_url=ctx.author.avatar_url)
        embed.set_footer(text="Momento")
        embed.add_field(name="Old Welcome Message", value=welcomeMessage)
        embed.add_field(name="New Welcome Message", value=value)
        await ctx.send(embed=embed)

    @commands.command()
    async def welcomeChannel(self, ctx: Context, channel: TextChannel):
        guildId = ctx.guild.id
        channelOld = await db.runCommand('getGuildWelcomeChannel', guildId)
        print(channelOld)
        if channelOld == None or channelOld == 0 or channelOld == "0" or channelOld == "None":
            channelOld = "No Channel Specified"
        elif channelOld != None or channelOld != "None":
            channelOld = channelOld[0]
            print(channelOld)
            channelOld = await self.bot.fetch_channel(channelOld)
            channelOld = channelOld.name
        channelNew = channel
        await self.db.runCommand('setGuildWelcomeChannel', guildId, channel.id)
        embed = discord.Embed(title="Welcomer Settings", colour=Colour(0x1e240),
                              timestamp=datetime.datetime.utcnow())
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.set_author(name=ctx.author.display_name + "#" + ctx.author.discriminator,
                         icon_url=ctx.author.avatar_url)
        embed.set_footer(text="Momento")
        embed.add_field(name="Old Welcome Channel", value=channelOld)
        embed.add_field(name="New Welcome Channel", value=channelNew.name)
        await ctx.send(embed=embed)

    @commands.command()
    async def welcomeEnabled(self, ctx: Context, value):
        """Enable of disable the welcoming of new members! use the words no, false or disabled for off or anything else for on"""
        guildId = ctx.guild.id

        if value == "false" or value == "no" or value == "disabled":
            yayornay = 0
        else:
            yayornay = 1
        await self.db.runCommand('setGuildWelcomeEnabled', guildId, yayornay)
        enabled = await db.runCommand('getGuildWelcomeEnabled', guildId)
        if enabled[0][0] == 0:
            enabledd = "Disabled"
        else:
            enabledd  = "Enabled"
        await self.db.runCommand('setGuildWelcomeEnabled', guildId, yayornay)
        embed = discord.Embed(title="Welcomer Settings", colour=Colour(0x1e240),
                              timestamp=datetime.datetime.utcnow())
        embed.set_thumbnail(url=ctx.author.avatar_url)
        embed.set_author(name=ctx.author.display_name + "#" + ctx.author.discriminator,
                         icon_url=ctx.author.avatar_url)
        embed.set_footer(text="Momento")
        embed.add_field(name="Welcomer Status", value=enabledd)
        await ctx.send(embed=embed)

    @Cog.listener()
    async def on_member_join(self, member: Member):
        guildId = member.guild.id
        enabled = await self.db.runCommand('getGuildWelcomeEnabled', guildId)
        await self.db.runCommand('setUserBase', member.id, guildId)
        if enabled[0][0] == 1:
            welcomeChannel = await self.db.runCommand('getGuildWelcomeChannel', guildId)
            welcomeMessage = await self.db.runCommand('getGuildWelcomeMessage', guildId)
            channel = await self.bot.fetch_channel(welcomeChannel[0])
            user_name = member.display_name
            user_discriminator = member.discriminator
            user_mention = member.mention
            guild_name = member.guild.name
            await channel.send(welcomeMessage[0][0].format(user_name=user_name, user_discriminator=user_discriminator, user_mention=user_mention, server_name=guild_name))


    @Cog.listener()
    async def on_member_leave(self, member: Member):
        await self.db.runCommand('removeUser', member.id, member.guild.id)



def setup(bot):
    bot.add_cog(Welcomer(bot))
    print(pcolours.HEADER + "Loading Cog: Welcomer" + pcolours.ENDC)