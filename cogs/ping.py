import asyncio

from discord.ext import commands
from discord_slash import SlashContext, cog_ext


class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        asyncio.create_task(self.bot.slash.sync_all_commands())

    def cog_unload(self):
        self.bot.slash.remove_cog_commands(self)

    @cog_ext.cog_slash(name="ping", description="このBotのレイテンシを返します。")
    async def slash_say(self, ctx: SlashContext):
        msg = await ctx.send("pong!")
        await msg.edit(content=f"pong!\n`{self.bot.ws.latency * 1000:.0f}ms`")


def setup(bot):
    bot.add_cog(Ping(bot))
