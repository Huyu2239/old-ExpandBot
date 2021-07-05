import os
from importlib import reload

import git
import libs
from discord.ext import commands


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.load_extension("cogs.management.eval")
        self.bot.load_extension("cogs.management.error_handler")
        self.repo = git.Repo()
        bot.libs = libs

    async def cog_check(self, ctx):
        return await self.bot.is_owner(ctx.author)

    @commands.command()
    async def git_pull(self, ctx):
        msg = await ctx.send("実行中・・・")
        self.repo.remotes.origin.pull()
        print("pulled")
        await msg.edit(content="完了")

    @commands.command()
    async def reload(self, ctx, arg=None):
        msg = await ctx.send("更新中")
        if arg == "libs":
            reload(libs)
            self.bot.libs = libs
        self.bot.reload_extension("cogs.management.error_handler")
        for cog in os.listdir("./cogs"):
            if cog.endswith(".py"):
                try:
                    self.bot.reload_extension(f"cogs.{cog[:-3]}")
                except commands.ExtensionNotLoaded:
                    self.bot.load_extension(f"cogs.{cog[:-3]}")
        await self.bot.change_presence(
            activity=discord.Game(
                name=f"/help | {len(self.guilds)}guilds"
            )
        )
        await msg.edit(content="更新しました")
        print("--------------------------------------------------")


def setup(bot):
    bot.add_cog(Admin(bot))
