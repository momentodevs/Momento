from aiohttp import ClientSession
from discord.ext.commands import AutoShardedBot

reserved = ["settings", "db", "aiohttp"]


class BasicBot(AutoShardedBot):
    """A revised commands.AutoShardedBot class to prevent overwriting reserved attributes in the basic bot"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.db = kwargs.get("db")
        self.settings = kwargs.get("settings")
        # self.aiohttp = ClientSession(loop=self.loop)

    def __setattr__(self, name, value):
        if name in reserved and hasattr(self, name):
            raise AttributeError(f"{name} is a reserved attribute")
        return super().__setattr__(name, value)