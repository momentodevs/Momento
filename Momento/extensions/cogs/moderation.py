import discord
import asyncio
import re
from better_profanity import profanity
from discord.abc import User
from discord.errors import Forbidden
from discord.ext import tasks, commands, menus
from discord.ext.commands import Cog
from discord.ext.commands.bot import AutoShardedBot
from discord.ext.commands.context import Context
from discord.ext.commands.converter import Converter, MemberConverter
from discord.ext.commands.errors import BadArgument, CheckFailure
from discord.member import Member
from discord.message import Message
from classes import pcolours


profanity.load_censor_words()

class Sinner(Converter):
    async def convert(self, ctx: Context, argument):
        argument = await commands.MemberConverter().convert(ctx, argument) # gets a member object
        permission = argument.guild_permissions.manage_messages # can change into any permission
        if not permission: # checks if user has the permission
            return argument # returns user object
        raise commands.BadArgument("You cannot punish other staff members") # tells user that target is a staff member

# Checks if you have a muted role
class Redeemed(Converter):
    async def convert(self, ctx: Context, argument):
        argument = await MemberConverter().convert(ctx, argument) # gets member object
        muted = discord.utils.get(ctx.guild.roles, name="Muted") # gets role object
        if muted in argument.roles: # checks if user has muted role
            return argument # returns member object if there is muted role
        raise commands.BadArgument("The user was not muted.") # self-explainatory


# Checks if there is a muted role on the server and creates one if there isn't
async def mute(ctx: Context, user: Member, reason):
    role = discord.utils.get(ctx.guild.roles, name="Muted") # retrieves muted role returns none if there isn't
    hell = discord.utils.get(ctx.guild.text_channels, name="hell") # retrieves channel named hell returns none if there isn't
    if not role: # checks if there is muted role
        try: # creates muted role
            muted = await ctx.guild.create_role(name="Muted", reason="To use for muting")
            for channel in ctx.guild.channels: # removes permission to view and send in the channels
                await channel.set_permissions(muted, send_messages=False,
                                              read_message_history=False,
                                              read_messages=False)
        except Forbidden:
            return await ctx.send("I have no permissions to make a muted role") # self-explainatory
        await user.add_roles(muted) # adds newly created muted role
        await ctx.send(f"{user.mention} has been sent to hell for {reason}")
    else:
        await user.add_roles(role) # adds already existing muted role
        await ctx.send(f"{user.mention} has been sent to hell for {reason}")

    if not hell: # checks if there is a channel named hell
        overwrites = {ctx.guild.default_role: discord.PermissionOverwrite(read_message_history=False),
                      ctx.guild.me: discord.PermissionOverwrite(send_messages=True),
                      muted: discord.PermissionOverwrite(read_message_history=True)} # permissions for the channel
        try: # creates the channel and sends a message
            channel = await ctx.create_channel('hell', overwrites=overwrites)
            await channel.send("Welcome to hell.. You will spend your time here until you get unmuted. Enjoy the silence.")
        except discord.Forbidden:
            return await ctx.send("I have no permissions to make #hell")



class Moderation(Cog):
    def __init__(self, bot: AutoShardedBot):
        self.bot = bot
        self.bot.db = self.db


    @commands.command()
    @commands.guild_only()
    @commands.bot_has_permissions(manage_messages=True)
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(rate=2, per=3, type=commands.BucketType.user)
    async def clear(self, ctx: Context, amount: int = 1):
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"<:greenTick:596576670815879169> {amount} messages have just been deleted")
        await asyncio.sleep(2)
        await ctx.channel.purge(limit=1)


    @commands.command()
    @commands.cooldown(rate=1, per=1, type=commands.BucketType.user)
    async def unmute(self, ctx: Context, user: Redeemed):
        """Unmutes a muted user"""
        await user.remove_roles(discord.utils.get(ctx.guild.roles, name="Muted")) # removes muted role
        await ctx.send(f"{user.mention} has been unmuted")


    @commands.command()
    @commands.cooldown(rate=1, per=1, type=commands.BucketType.user)
    async def mute(self, ctx: Context, user: Sinner, reason=None):
        """Gives them hell."""
        await mute(ctx, user, reason or "treason") # uses the mute function

    #anti-advertisement(only listens for discord links) and profanity filter(check profanity.txt)
    @commands.Cog.listener()
    @commands.bot_has_permissions(manage_messages=True)
    @commands.has_permissions(manage_messages=True)
    async def on_message(self, message: Message):
        if not message.author.bot:
            urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',message.content.lower())
            if urls is not None and message.content.startswith('https://discord.gg' or 'http://discord.gg'):
                await message.delete()
                await message.channel.send("Links are not allowed!")
                return

            elif profanity.contains_profanity(message.content):
                await message.delete()
                await message.channel.send("Profanity in this server is not allowed!")

        else:
            pass



def setup(bot):
    bot.add_cog(Moderation(bot))
    print(pcolours.HEADER + "Loading Cog: Moderation" + pcolours.ENDC)
