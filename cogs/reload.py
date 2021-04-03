from discord.ext import commands
import json
import os


class Reload(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        return await self.bot.is_owner(ctx.author)

    @commands.command()
    async def reload(self, ctx, _json):
        msg = await ctx.send('更新中')
        if _json == 'true':
            with open(f'{self.bot.data_directory}settigs.json') as f:
                self.bot.expand = json.load(f)
        for cog in os.listdir('./cogs'):
            if cog.endswith('.py'):
                if cog == 'reload.py':
                    continue
                try:
                    self.bot.reload_extension(f'cogs.{cog[:-3]}')
                except commands.ExtensionNotLoaded:
                    self.bot.load_extension(f'cogs.{cog[:-3]}')
        await msg.edit(content='更新しました')


def setup(bot):
    bot.add_cog(Reload(bot))
