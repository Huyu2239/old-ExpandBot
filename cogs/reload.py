import json
import os

from discord.ext import commands


class Reload(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        return await self.bot.is_owner(ctx.author)

    @commands.command()
    async def reload(self, ctx, path=None):
        msg = await ctx.send('更新中')

        if path == 'full' or 'lib':
            self.bot.get_cog('Expand').reload_libs()
            self.bot.get_cog('Mute').reload_libs()
        if path == 'full' or 'json':
            with open(f'{self.bot.data_directory}guilds_data.json') as f:
                self.bot.guild_open = json.load(f)
            with open(f'{self.bot.data_directory}mute_data.json') as f:
                self.bot.embed_type = json.load(f)
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
        await msg.edit(content='更新しました')
        print('--------------------------------------------------')


def setup(bot):
    bot.add_cog(Reload(bot))
