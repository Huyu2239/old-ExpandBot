from discord.ext import commands
import discord


class Presence(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def on_guild_join(self, _):
        await self.bot.change_presence(
            activity=discord.Game(name=f"/ヘルプ | {len(self.bot.guilds)}サーバー")
        )

    async def on_guild_remove(self, _):
        await self.bot.change_presence(
            activity=discord.Game(name=f"/ヘルプ | {len(self.bot.guilds)}サーバー")
        )


def setup(bot):
    bot.add_cog(Presence(bot))
