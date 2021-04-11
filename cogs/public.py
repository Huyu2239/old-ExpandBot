import discord
from discord.ext import commands  # , tasks
from discord_slash import SlashContext, cog_ext  # SlashCommand
# from discord_slash.utils import manage_commands

import asyncio
import json


class Public(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        asyncio.create_task(self.bot.slash.sync_all_commands())

    def cog_unload(self):
        self.bot.slash.remove_cog_commands(self)

    @cog_ext.cog_slash(
        name='public',
        description='サーバー外メッセージリンクの展開の**ON・OFF**を切り替えます'
    )
    async def slash_say(self, ctx: SlashContext):
        embed = ''
        if ctx.guild.id not in self.bot.guild_open:
            self.bot.guild_open.append(ctx.guild.id)
            embed = discord.Embed(description='サーバー外メッセージリンクの展開を**ON**にしました')
        else:
            self.bot.guild_open.remove(ctx.guild.id)
            embed = discord.Embed(description='サーバー外メッセージリンクの展開を**OFF**にしました')
        await ctx.send(embed=embed)
        with open(f'{self.bot.data_directory}guild_open.json', 'w') as f:
            json.dump(self.bot.guild_open, f, indent=4)


def setup(bot):
    bot.add_cog(Public(bot))
