from discord.ext import commands


class Del(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_rection_add(self, payload):
        return


def setup(bot):
    bot.add_cog(Del(bot))
