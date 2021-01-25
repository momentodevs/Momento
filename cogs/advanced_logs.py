import discord 
from discord import commands
from discord_webhook import DiscordWebhook, DiscordEmbed
import logging

class Logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        logger = logging.getLogger('discord')
        logger.setLevel(logging.DEBUG)

        webhook = DiscordWebhook(url='URL_HERE')

        # create embed object for webhook
        embed = DiscordEmbed(title='Momento Error Logs', description='', color=242424)

        # set author
        embed.set_author(name='TimmyTime#0310')

        # set image
        #embed.set_image(url='your image url')

        # set thumbnail
        #embed.set_thumbnail(url='your thumbnail url')

        # set footer
        embed.set_footer(text='Copyright | Momento')

        # set timestamp (default is now)
        embed.set_timestamp()

        # add fields to embed

        embed.add_embed_field(name="Traceback", value=f'Error Name: {logging.error.__name__}\nMessage: {logging.error.__doc__}\nModule: {logging.error.__module__}')

        # add embed object to webhook
        webhook.add_embed(embed)

        response = webhook.execute()
