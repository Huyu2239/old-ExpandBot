from discord.ext import commands
import re

from lib.embed import compose_embed

regex_discord_message_url = (
    'https://(ptb.|canary.)?discord(app)?.com/channels/'
    '(?P<guild>[0-9]{18})/(?P<channel>[0-9]{18})/(?P<message>[0-9]{18})'
)


class Expand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def check_mute(self, message):
        md = self.bot.mute_data
        if message.guild.id in md.get('guilds'):
            return True
        if message.channel.id in md.get('channels'):
            return True
        for role in message.author.roles:
            if role.id in md.get('roles'):
                return True
        if message.author.id in md.get('users'):
            return True

    async def find_messages(self, message):  # message.contentの中から正規表現でURLを抜き出し、メッセージオブジェクトをリストに入れて返す
        messages = []
        for ids in re.finditer(regex_discord_message_url, message.content):
            if message.guild.id != int(ids['guild']):
                if await self.check_hidden(message, int(ids['guild'])):
                    return
            fetched_message = await self.fetch_message_from_id(
                guild=self.bot.get_guild(int(ids['guild'])),
                channel_id=int(ids['channel']),
                message_id=int(ids['message']),
            )
            messages.append(fetched_message)
        return messages

    async def check_hidden(self, message, target_guild_id):
        return True   # 非公開
        '''
        if (message.guild.id and target_guild_id) in self.bot.guild_open:
            return True
        else:
            return False
        '''

    async def fetch_message_from_id(self, guild, channel_id, message_id):
        channel = guild.get_channel(channel_id)
        try:
            message = await channel.fetch_message(message_id)
        except Exception:
            return
        return message

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if await self.check_mute(message):
            return
        messages = await self.find_messages(message)
        if messages is None:
            return
        for m in messages:
            if m.content:
                embed_message = await compose_embed(m, message.guild.id)
                if embed_message[1] == 2:  # webhook型
                    return
                await message.channel.send(embed=embed_message[0])
            for embed in m.embeds:
                await message.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Expand(bot))
