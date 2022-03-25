import os
from importlib import reload

import git
import libs
from discord.ext import commands
import discord


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.repo = git.Repo()

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
            for lib in os.listdir("./libs"):
                if lib.endswith(".py") and lib != "__init__.py":
                    reload(getattr(libs, lib[:-3]))
            reload(libs)
        for folder in self.bot.cog_folders:
            if folder == "management":
                continue
            for cog in os.listdir(f"./{folder}"):
                if cog == "__pycache__":
                    continue
                try:
                    self.bot.reload_extension(f"{folder}.{cog[:-3]}")
                except discord.ext.commands.errors.ExtensionNotLoaded:
                    self.bot.load_extension(f"{folder}.{cog[:-3]}")
        await self.bot.change_presence(
            activity=discord.Game(name=f"/ヘルプ | {len(self.bot.guilds)}guilds")
        )
        await msg.edit(content="更新しました")
        print("--------------------------------------------------")


def setup(bot):
    bot.add_cog(Admin(bot))
