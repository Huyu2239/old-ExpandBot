import os
from importlib import reload

import git
import lib.check
import lib.database
import lib.embed
from discord.ext import commands


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.load_extension("cogs.management.eval")
        self.bot.load_extension("cogs.management.error_handler")
        self.repo = git.Repo()
        bot.Check = lib.check.Check
        bot.database = lib.database
        bot.embed = lib.embed

    async def cog_check(self, ctx):
        return await self.bot.is_owner(ctx.author)

    @commands.command()
    async def git_pull(self, ctx):
        msg = await ctx.send("実行中・・・")
        self.repo.remotes.origin.pull()
        print("pulled")
        await msg.edit(content="完了")

    @commands.command()
    async def reload(self, ctx, path=None):
        msg = await ctx.send("更新中")
        if path == "lib":
            reload(lib.check)
            self.bot.Check = lib.check.Check
            reload(lib.database)
            self.bot.database = lib.database
            reload(lib.embed)
            self.bot.embed = lib.embed
        for cog in os.listdir("./cogs"):
            if cog.endswith(".py"):
                try:
                    self.bot.unload_extension(f"cogs.{cog[:-3]}")
                except commands.ExtensionNotLoaded:
                    pass
                try:
                    self.bot.load_extension(f"cogs.{cog[:-3]}")
                except commands.ExtensionAlreadyLoaded:
                    self.bot.reload_extension(f"cogs.{cog[:-3]}")
        await msg.edit(content="更新しました")
        print("--------------------------------------------------")


def setup(bot):
    bot.add_cog(Admin(bot))
