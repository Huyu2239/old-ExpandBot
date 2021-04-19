from discord.ext import commands
import re

from lib.embed import compose_embed

regex_discord_message_url = (
    'https://(ptb.|canary.)?discord(app)?.com/channels/'
    '(?P<guild>[0-9]{18})/(?P<channel>[0-9]{18})/(?P<message>[0-9]{18})'
)


class Expand(commands.Cog):
    '''
    message: on_messageの引数によるMessageObject
    msg(msgs): fetchするMessageObject
    chech_hoge: 当てはまる時にTrue
    '''
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

    async def find_msgs(self, message):
        msgs = []
        for ids in re.finditer(regex_discord_message_url, message.content):
            if message.guild.id != int(ids['guild']):
                msg_hidden = await self.check_hidden(message, int(ids['guild']))
                if msg_hidden is True:
                    continue
            fetched_msg = await self.fetch_msg_with_id(
                guild=self.bot.get_guild(int(ids['guild'])),
                channel_id=int(ids['channel']),
                message_id=int(ids['message']),
            )
            msgs.append(fetched_msg)
        return msgs

    async def check_hidden(self, message, target_guild_id):
        return True   # 非公開

    async def fetch_msg_with_id(self, guild, channel_id, message_id):
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
        msgs = await self.find_msgs(message)
        if msgs is None:
            return
        for msg in msgs:
            if msg.content:
                embed_message = await compose_embed(self, msg, message)
                await message.channel.send(embed=embed_message[0])
            for embed in msg.embeds:
                await message.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Expand(bot))
