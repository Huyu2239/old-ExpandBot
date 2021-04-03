from discord.ext import commands
from dispander import dispand


class Expand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.guild_only()
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author is self.bot.user:
            return
        await dispand(message)


def setup(bot):
    bot.add_cog(Expand(bot))
