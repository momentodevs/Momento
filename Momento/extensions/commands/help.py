import collections
import discord
from discord.ext import commands
from discord.ext.commands import converter

EXCLUDED_COMMANDS = ['help']


async def _can_run(ctx, cmd):
    try:
        return await cmd.can_run(ctx)
    except commands.CommandError:
        return False


class Help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.bot.db = self.db

    @commands.command()
    async def help(self, ctx, *, command_name=None):

        if not command_name:
            output = await self._help_global(ctx)
        else:
            cmd = self.bot.get_command(command_name)
            if not cmd or cmd.name in EXCLUDED_COMMANDS or cmd.hidden or not await _can_run(ctx, cmd):
                return
            if isinstance(cmd, commands.GroupMixin):
                output = await self._help_group(ctx, cmd)
            else:
                output = await self._help_command(ctx, cmd)

        if output:
            if isinstance(output, str):
                await ctx.send(output)
            else:
                await ctx.send(embed=output)

    async def _help_global(self, ctx):
        filtered_commands = [cmd for cmd in self.bot.commands
                             if cmd.name.lower() not in EXCLUDED_COMMANDS
                             and not cmd.hidden
                             and await _can_run(ctx, cmd)]

        command_tree = collections.defaultdict(list)

        for cmd in filtered_commands:
            cog_name = getattr(cmd.cog, "display_name", cmd.cog_name)
            command_tree[cog_name].append(cmd)

        embed = discord.Embed(name="Momento Help", description="Commands for Momento", color=discord.Colour.green())
        output = ''
        for cog_name in sorted(command_tree):
            cmds = command_tree[cog_name]
            formatted_cmds = [f"`{cmd.name}`" for cmd in sorted(cmds, key=lambda cmd: cmd.name)]
            #output += f"**{cog_name}**\n"
            output = ", ".join(formatted_cmds) + "\n\n"
            embed.add_field(name=cog_name, value=output, inline=False)
        embed.set_footer(text="Momento")
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        return embed

    async def _help_group(self, ctx, cmd):
        output = ''
        if getattr(cmd, 'invoke_without_command', False):
            embed = discord.Embed(title=f"Help For {cmd.name}", color=discord.Colour.green(),
                                  description=getattr(cmd, 'help', "") + "\n\n")
            usage = cmd.usage or f"{cmd.name} {cmd.signature}"
            embed.add_field(name="Usage", value=f'{ctx.prefix}{usage}\n\n')
        #output = await converter.clean_content().convert(ctx, output)
        embed = discord.Embed(title=f"Help For {cmd.name}", color=discord.Colour.green(),description=f"**Commands** (_type `m?{cmd.name} <command>` with `<command>` a command from the list_)\n")
        formatted_cmds = [cmd for cmd in sorted(cmd.commands, key=lambda cmd: cmd.name)]
        for formatted_cmd in formatted_cmds:
            usage = formatted_cmd.usage or f"{formatted_cmd.name} {formatted_cmd.signature}"
            embed.add_field(name=formatted_cmd.name, value=usage, inline=False)
        embed.set_footer(text="Momento")
        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        return embed

    async def _help_command(self, ctx, cmd):
        output = getattr(cmd, 'help', "") + "\n\n"
        usage = cmd.usage or f"{cmd.name} {cmd.signature}"
        output += f"**Usage:** `{ctx.prefix}{cmd.full_parent_name} {usage}`"
        output = await converter.clean_content().convert(ctx, output)
        return output


def setup(bot):
    bot.add_cog(Help(bot))