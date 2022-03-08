import json
import os
import platform
import random
import sys

import nextcord
from nextcord import Interaction
from nextcord.ext import tasks, commands
from nextcord.ext.commands import Bot
from nextcord.ext.commands import Context

import exceptions

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)

"""
Setup Bot Intents (event restrictions)
For more information about Intents, go to the following websites
https://docs.disnake.dev/en/latest/intents.html
https://docs.disnake.dev/en/latest/intents.html#privileged-intents


Default Intents:
intents.bans = True
intents.dm_messages = False
intents.dm_reactions = False
intents.dm_typing = False
intents.emojis = True
intents.guild_messages = True
intents.guild_reactions = True
intents.guild_typing = False
intents.guilds = True
intents.integrations = True
intents.invites = True
intents.reactions = True
intents.typing = False
intents.voice_states = False
intents.webhooks = False
Privileged Intents (Needs to be enabled on dev page), please use them only if you need them:
intents.members = True
intents.messages = True
intents.presences = True
"""

intents = nextcord.Intents.default()

bot = Bot(command_prefix=commands.when_mentioned_or(config["prefix"]), intents=intents)


@bot.event
async def on_ready() -> None:
    """
    The Code in this Event is Executed when the bot is ready
    """
    print(f"Logged in as {bot.user.name}")
    print(f"nextcord API version {nextcord.__version__}")
    print(f"Python Version {platform.python_version()}")
    print(f"Running on {platform.system()} {platform.release()} ({os.name})")
    print("----------------------")
    status_task.start()


@tasks.loop(minutes=1)
async def status_task() -> None:
    """
    Setup the game status task of the Bot
    """
    statuses = ["with you!", f"watching over {len(bot.users)}"]
    await bot.change_presence(activity=nextcord.Game(random.choice(statuses)))

# Removes the default help command of discord.py to be able to create our custom help command.
bot.remove_command("help")


def load_commands(command_type: str) -> None:
    for file in os.listdir(f"./cogs/{command_type}"):
        if file.endswith(".py"):
            extension = file[:-3]
            try:
                bot.load_extension(f"cogs.{command_type}.{extension}")
                print(f"Loaded Extension '{extension}'")
            except Exception as e:
                exception = f"{type(e).__name__}: {e}"
                print(f"Failed to load Extension {extension}\n{exception}")


if __name__ == "__main__":
    """
    This will automatically load slash commands and normal commands located in their respective folder.
    
    If you want to remove slash commands, which is not recommended due to their Message Intent being a privileged Intent,
    you can remove the loading of slash commands Below
    """

    load_commands("slash")
    load_commands("normal")


@bot.event
async def on_message(message: nextcord.Message) -> None:
    """
    The code in this event is executed every time someone sends a message, with or without the prefix
    :param message: The message that was Sent
    """
    if message.author == bot.user or message.author.bot:
        return
    await bot.process_commands(message)


@bot.event
async def on_slash_command(interaction: Interaction) -> None:
    """
    The code in this event is executed every time a slash command has been *succesfully* executed
    :param interaction: The slash command that was executed
    """
    print(
        f"Executed {interaction.data['name']} command in {interaction.guild.name} (ID: {interaction.guild.id}) by {interaction.user.name} (ID: {interaction.user.id})"
    )


@bot.event
async def on_slash_command_error(interaction: Interaction, error: Exception) -> None:
    """
    The code in this event is executec every time a valid slash command catches an error
    :param interaction: The slash command that failed executing
    :param error: The error that has been faced
    """
    if isinstance(error, exceptions.UserBlacklisted):
        """
        The code here will only execute if the error is an instance of ' UserBlacklisted', which can occur when using
        the @checks.is_owner() check in your command, or you can raise the error by yourself.
        
        'hidden=True' will make it so that only the user who executes the command can see the message
        """
        embed = nextcord.Embed(
            title="Error!",
            description="You are blacklisted from using the bot.",
            color=0xE02B2B
        )
        print("A Blacklisted user tried to execute a command.")
        return await interaction.send(embed=embed, ephemeral=True)
    elif isinstance(error, commands.MissingPermissions):
        embed = nextcord.Embed(
            title="Error!",
            description="You are missing the permission(s) `" + ",".join(
                error.missing_permissions) + "` to execute this command!",
            color=0xE02B2B
        )
        print("A Blacklisted user tried to execute a command")
        return await interaction.send(embed=embed, ephemeral=True)
    raise error


@bot.event
async def on_command_completion(context: Context) -> None:
    """
    The code in this event is executed every time a normal command has been *succesfully* executed
    :param context: The context of the command that has been executed
    """
    full_command_name = context.command.qualified_name
    split = full_command_name.split(" ")
    executed_command = str(split[0])
    print(
        f"Executed {executed_command} command in {context.guild.name} (ID: {context.message.guild.id}) by {context.message.author.display_name} (ID: {context.message.author.id})"
    )


@bot.event
async def on_command_error(context: Context, error) -> None:
    """
    The code in this event executes everytime a normal valid command catches an error
    :param context: The normal command that failed executing.
    :param error: The error that has been faced.
    """
    if isinstance(error, commands.CommandOnCooldown):
        minutes, seconds = divmod(error.retry_after, 60)
        hours, minutes = divmod(minutes, 60)
        hours = hours % 24
        embed = nextcord.Embed(
            title="Hey, please slow down!",
            description=f"You can use this command again in {f'{round(hours)} hours' if round(hours) > 0 else ''} {f'{round(minutes)} minutes' if round(minutes) > 0 else ''} {f'{round(seconds)} seconds' if round(seconds) > 0 else ''}.",
            color=0xE02B2B
        )
        await context.send(embed=embed)
    elif isinstance(error, commands.MissingPermissions):
        embed = nextcord.Embed(
            title="Error!",
            description="You are missing the permission(s) `" + ", ".join(
                error.missing_permissions) + "` to execute this command!",
            color=0xE02B2B
        )
        await context.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = nextcord.Embed(
            title="Error!",
            description=str(error).capitalize(),
            # We need to capitalize because the command arguments have no capital letter in the code.
            color=0xE02B2B
        )
        await context.send(embed=embed)
    raise error

bot.run(config['token'])
