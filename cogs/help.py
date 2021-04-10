# import discord
from discord.ext import commands  # , tasks
from discord_slash import SlashContext, cog_ext  # SlashCommand
# from discord_slash.utils import manage_commands

import asyncio


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        asyncio.create_task(self.bot.slash.sync_all_commands())

    def cog_unload(self):
        self.bot.slash.remove_cog_commands(self)

    @cog_ext.cog_slash(name='help', description='このBotのHelpを返します。', guild_ids=[829431106263580703])
    async def slash_say(self, ctx: SlashContext):
        # await ctx.respond(eat=True)
        await ctx.send('help')


def setup(bot):
    bot.add_cog(Help(bot))
