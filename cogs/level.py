import discord
from discord.ext import commands
import psycopg2
import sys, os
import numpy as np
import pandas as pd
import example_psql as creds
import pandas.io.sql as psql

class Level(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


def setup(client):
    bot.add_cog(Level(bot))
