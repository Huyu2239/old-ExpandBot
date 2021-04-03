import json
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
if os.name == 'nt':
    data_directory = 'json\\'
else:
    data_directory = 'json/'


class Mochi(commands.Bot):
    def __init__(self, command_prefix, **options):
        self.command_prefix = command_prefix
        prefix = commands.when_mentioned_or(command_prefix)
        allowed_mentions = discord.AllowedMentions(everyone=False, roles=False, users=True)
        intents = discord.Intents.all()
        super().__init__(
            command_prefix=prefix,
            intents=intents,
            allowed_mentions=allowed_mentions,
            **options
        )
        self.remove_command('help')
        self.data_directory = data_directory
        with open(f'{self.data_directory}settings.json') as f:
            self.data = json.load(f)

    async def on_ready(self):
        for cog in os.listdir("./cogs"):
            if cog.endswith(".py"):
                try:
                    self.load_extension(f"cogs.{cog[:-3]}")
                except commands.ExtensionAlreadyLoaded:
                    self.reload_extension(f"cogs.{cog[:-3]}")
                except discord.ext.commands.errors.ExtensionFailed:
                    continue
        print('ready')
        await self.change_presence(activity=discord.Game(name=f"e:help | {len(self.guilds)}guilds"))

    async def on_guild_join(self, _):
        await self.change_presence(activity=discord.Game(name=f"e:help | {len(self.guilds)}guilds"))

    async def on_guild_remove(self, _):
        await self.change_presence(activity=discord.Game(name=f"e:help | {len(self.guilds)}guilds"))


if __name__ == '__main__':
    bot = Mochi(command_prefix="e:")
    bot.run(os.environ['TOKEN'])
