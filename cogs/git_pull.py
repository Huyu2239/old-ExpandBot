import git
from discord.ext import commands


class Git(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        repo = git.Repo()
        self.ExpandBot = repo.remotes.origin

    async def cog_check(self, ctx):
        return await self.bot.is_owner(ctx.author)

    @commands.command()
    async def git_pull(self, ctx):
        msg = await ctx.send('実行中・・・')
        self.ExpandBot.pull()
        print('pulled')
        await msg.edit(content='完了')


def setup(bot):
    bot.add_cog(Git(bot))
