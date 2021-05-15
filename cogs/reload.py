import json
import os
from discord.ext import commands
from importlib import reload
import lib.check
import lib.database
import lib.embed


class Reload(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        bot.check = lib.check
        bot.database = lib.database
        bot.embed = lib.embed

    async def cog_check(self, ctx):
        return await self.bot.is_owner(ctx.author)

    @commands.command()
    async def reload(self, ctx, path=None):
        msg = await ctx.send('更新中')

        for cog in os.listdir('./cogs'):
            if cog.endswith('.py'):
                if cog == 'reload.py':
                    continue
                try:
                    self.bot.unload_extension(f'cogs.{cog[:-3]}')
                except commands.ExtensionNotLoaded:
                    pass
                try:
                    self.bot.load_extension(f'cogs.{cog[:-3]}')
                except commands.ExtensionAlreadyLoaded:
                    self.bot.reload_extension(f'cogs.{cog[:-3]}')
        if path == ('full' or 'lib'):
            reload(lib.check)
            self.bot.check = lib.check
            reload(lib.database)
            self.bot.database = lib.database
            reload(lib.embed)
            self.bot.embed = lib.embed
        if path == ('full' or 'json'):
            with open(f'{self.bot.data_directory}guilds_data.json') as f:
                self.bot.guild_open = json.load(f)
            with open(f'{self.bot.data_directory}mute_data.json') as f:
                self.bot.embed_type = json.load(f)

        await msg.edit(content='更新しました')
        print('--------------------------------------------------')


def setup(bot):
    bot.add_cog(Reload(bot))
