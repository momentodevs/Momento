import discord
import time
import sqlite3
import asyncio
import random
import os
from discord import Member, Embed
from discord.ext.commands import Cog
from typing import Optional
from os.path import isfile
from datetime import datetime, timedelta
from discord.ext.menus import MenuPages, ListPageSource
from discord.ext import commands
from db import db

class Level(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # @commands.Cog.listener()
    # async def on_ready(self, bot):
    #     credentials = {"user": "USERNAME", "password": "PASSWORD", "database": "DATABSE", "host": "127.0.0.1"}
    #      try:
    #          await db.start(config.token)
    #      except KeyboardInterrupt:
    #          await db.close()
    #          await bot.logout()
    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            db.connect("./data/database.db")
            result = db.record("SELECT UserID FROM users WHERE UserID = (?)", message.author.id)
            if result is not None:
                xp, lvl, xplock = db.record("SELECT XP, Level, XPLock FROM users WHERE UserID = ?", message.author.id)
                if datetime.utcnow() > datetime.fromisoformat(xplock):

                    xp_to_add = random.randint(10, 20)
                    new_lvl = int(((xp + xp_to_add) // 42) ** 0.55)

                    db.execute("UPDATE users SET XP = XP + ?, Level = ?, XPLock = ? WHERE UserID = ?",
                        xp_to_add,
                        new_lvl,
                        (datetime.utcnow() + timedelta(seconds=50)).isoformat(),
                        message.author.id,
                    )
                    db.commit()

                    if new_lvl > lvl:
                        await message.channel.send(f":partying_face: {message.author.mention} has leveled up to {new_lvl:,}!")


                        #a autorole example(copied from my bot(obviously u'd need some guild sorting to do, but if u need autoroles, heres a start))
                        # if new_lvl == 5:
                        #     new_here = message.guild.get_role(791162885002100793)
                        #     await message.author.remove_role(new_here)
                        #     white_belt = message.guild.get_role(791161672957558834)
                        #     await message.author.add_roles(white_belt)
                        #     print(colored(f"[level]: Added {white_belt.name} to {message.author.name}...", "cyan"))
                        #     await message.author.send(f":partying_face: Hooray, you have gotten the {white_belt.name} role!")
                        #
                        # elif new_lvl == 10:
                        #     yellow_belt = message.guild.get_role(791161670080004126)
                        #     await message.author.add_roles(yellow_belt)
                        #     print(colored(f"[level]: Added {yellow_belt.name} to {message.author.name}...", "cyan"))
                        #     await message.author.send(f":partying_face: Hooray, you have gotten the {yellow_belt.name} role!")
                        #
                        # elif new_lvl == 20:
                        #     orange_belt = message.guild.get_role(791161667148840970)
                        #     await message.author.add_roles(orange_belt)
                        #     print(colored(f"[level]: Added {orange_belt.name} to {message.author.name}...", "cyan"))
                        #     await message.author.send(f":partying_face: Hooray, you have gotten the {orange_level.name} role!")
                        #
                        # elif new_lvl == 30:
                        #     green_belt = message.guild.get_role(791161664296058890)
                        #     await message.author.add_roles(green_belt)
                        #     print(colored(f"[level]: Added {green_belt.name} to {green_belt.author.name}...", "cyan"))
                        #     await message.author.send(f":partying_face: Hooray, you have gotten the {green_belt.name} role!")
                        #
                        # elif new_lvl == 40:
                        #     blue_belt = message.guild.get_role(791161661293330432)
                        #     await message.author.add_roles(blue_belt)
                        #     print(colored(f"[level]: Added {blue_belt.name} to {blue_belt.author.name}...", "cyan"))
                        #     await message.author.send(f":partying_face: Hooray, you have gotten the {blue_belt.name} role!")
                        #
                        # elif new_lvl == 50:
                        #     purple_belt = message.guild.get_role(791161658406993940)
                        #     await message.author.add_roles(purple_belt)
                        #     print(colored(f"[level]: Added {purple_belt.name} to {purple_belt.author.name}...", "cyan"))
                        #     await message.author.send(f":partying_face: Hooray, you have gotten the {purple_belt.name} role!")
                        #
                        # elif new_lvl == 75:
                        #     black_belt = message.guild.get_role(791161652971962378)
                        #     await message.author.add_roles(black_belt)
                        #     print(colored(f"[level]: Added {black_belt.name} to {black_belt.author.name}...", "cyan"))
                        #     await message.author.send(f":partying_face: Hooray, you have gotten the {black_belt.name} role!")
                        #
                        # elif new_lvl == 100:
                        #     moderator = message.guild.get_role(791161649901207572)
                        #     await message.author.add_roles(moderator)
                        #     print(colored(f"[level]: Added {moderator.name} to {moderator.author.name}...", "cyan"))
                        #     await message.author.send(f":partying_face: Hooray, you have gotten the {moderator.name} role!")

                else:
                    pass

            else:
                db.execute("INSERT OR IGNORE INTO users (UserID) VALUES (?)", message.author.id)
                db.commit()


def setup(client):
    bot.add_cog(Level(bot))
