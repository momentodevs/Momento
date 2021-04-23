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
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import mysql.connector

# mysql login.
mydb = mysql.connector.connect(
  host="localhost",
  user="yourusername",
  password="yourpassword"
)
mycursor = mydb.cursor()

# print(mydb) 

class Menu(ListPageSource):
    def __init__(self, ctx, data):
        self.ctx = ctx

        super().__init__(data, per_page=10)

    async def write_page(self, menu, offset, fields=[]):
        offset = (menu.current_page * self.per_page) + 1
        len_data = len(self.entries)

        embed = Embed(
            title="Leaderboard",
            colour=self.ctx.author.colour,
        )

        embed.set_thumbnail(url=self.ctx.guild.me.avatar_url)
        embed.set_footer(
            text=f"{offset:,} - {min(len_data, offset+self.per_page-1):,} of {len_data:,} members."
        )

        for name, value in fields:
            embed.add_field(name=name, value=value, inline=False)

        return embed

    async def format_page(self, menu, entries):
        offset = (menu.current_page * self.per_page) + 1
        fields = []
        table = "\n".join(
            f"{idx+offset}. **{self.ctx.guild.get_member(entry[0]).name}** ~ `{entry[1]}`"
            for idx, entry in enumerate(entries)
        )

        fields.append(("Top members:", table))

        return await self.write_page(menu, offset, fields)

class Level(Cog):
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
    @Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            result = mycursor.execute("SELECT UserID FROM users WHERE UserID = (?)", message.author.id)
            if result is not None:
                xp, lvl, xplock = mycursor.execute("SELECT XP, Level, XPLock FROM users WHERE UserID = ?", message.author.id)
                if datetime.utcnow() > datetime.fromisoformat(xplock):

                    xp_to_add = random.randint(10, 20)
                    new_lvl = int(((xp + xp_to_add) // 42) ** 0.55)

                    mycursor.execute("UPDATE users SET XP = XP + ?, Level = ?, XPLock = ? WHERE UserID = ?",
                        xp_to_add,
                        new_lvl,
                        (datetime.utcnow() + timedelta(seconds=50)).isoformat(),
                        message.author.id,
                    )
                    mydb.commit()

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
                mycursor.execute("INSERT OR IGNORE INTO users (UserID) VALUES (?)", message.author.id)
                mydb.commit()

    @commands.command()
    async def rank(self, ctx, target: Optional[Member]):
        target = target or ctx.author
        ids = mycursor.execute("SELECT UserID FROM users ORDER BY XP DESC")

        xp, lvl = mycursor.execute(
            "SELECT XP, Level FROM users WHERE UserID = ?", target.id
        ) or (None, None)

        if lvl is not None:
            await ctx.channel.send(f"`Global Rank`\n{target.display_name} is level {lvl:,} with {xp:,} xp and is rank {ids.index(target.id)+1} of {len(ids):,} users globally.")

    @commands.command()
    async def leaderboard(self, ctx):
        records = mycursor.execute("SELECT UserID, XP FROM users ORDER BY XP DESC")
        menu = MenuPages(source=Menu(ctx, records), clear_reactions_after=True, timeout=100.0)
        await menu.start(ctx)
        
     @commands.command()
    async def rank(self, context, target: Optional[Member]):
        print(colored(f"[level]: {context.author} accessed rank...", "cyan"))
        target = target or context.author

        result = db.record(f"SELECT XP, Level FROM users WHERE UserID = {target.id}")

        if result is not None:
            async with context.typing():
                await asyncio.sleep(1)

                img = Image.open("./data/rank.png")
                draw = ImageDraw.Draw(img)
                font = ImageFont.truetype("./data/Quotable.otf", 35)
                font1 = ImageFont.truetype("./data/Quotable.otf", 24)
                async with aiohttp.ClientSession() as session:
                    async with session.get(str(context.author.avatar_url)) as response:
                        image = await response.read()
                icon = Image.open(BytesIO(image)).convert("RGBA")
                img.paste(icon.resize((156, 156)), (50, 60))
                draw.text((242, 100), f"{str(result[1])}", (140, 86, 214), font=font)
                draw.text((242, 180), f"{str(result[0])}", (140, 86, 214), font=font)
                draw.text((50,220), f"{context.author.name}", (140, 86, 214), font=font1)
                draw.text((50,240), f"#{context.author.discriminator}", (255, 255, 255), font=font1)
                img.save("./data/infoimg2.png")
                ffile = discord.File("./data/infoimg2.png")
                await context.send(file=ffile)

        else:
            async with context.typing():
                await asyncio.sleep(1)
                await context.channel.send("You are not in the database :(")


def setup(bot):
    bot.add_cog(Level(bot))
