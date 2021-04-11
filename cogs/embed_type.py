# import discord
from discord.ext import commands  # , tasks
from discord_slash import SlashContext, cog_ext  # SlashCommand
# from discord_slash.utils import manage_commands

import asyncio
# import json


class Public(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        asyncio.create_task(self.bot.slash.sync_all_commands())

    def cog_unload(self):
        self.bot.slash.remove_cog_commands(self)

    @cog_ext.cog_slash(
        name='embed_type',
        description='展開メッセージの見た目を変更します'
    )
    async def slash_say(self, ctx: SlashContext):
        await ctx.send('embed_type')


def setup(bot):
    bot.add_cog(Public(bot))
