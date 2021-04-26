import importlib
import re

import discord
import libs.embed
from discord.ext import commands

regex_discord_message_url = (
    'https://(ptb.|canary.)?discord(app)?.com/channels/'
    '(?P<guild>[0-9]{18})/(?P<channel>[0-9]{18})/(?P<message>[0-9]{18})'
)


class Expand(commands.Cog):
    '''
    message: on_messageの引数によるMessageObject
    msg(msgs): 引用されたMessageObject
    m :botが送信したMessageObject
    check_hoge: 当てはまる時にTrue
    '''
    def __init__(self, bot):
        self.bot = bot

    def reload_libs(self):
        importlib.reload(libs.embed)

    async def check_mute(self, message):
        md = self.bot.mute_data
        if message.guild:
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
        msgs = list()
        for ids in re.finditer(regex_discord_message_url, message.content):
            msg = await self.fetch_msg_with_id(
                msg_guild=self.bot.get_guild(int(ids['guild'])),
                msg_channel_id=int(ids['channel']),
                msg_id=int(ids['message']),
            )
            if message.guild.id != int(ids['guild']):
                message_hidden = await self.check_hidden(message)
                if message_hidden is True:
                    continue
                else:
                    msg_hidden = await self.check_hidden(msg)
                    if msg_hidden is True:
                        continue
            msgs.append(msg)
        return msgs

    async def check_hidden(self, m):
        # サーバー設定
        if self.bot.guilds_data.get(str(m.guild.id)) is None:
            return True
        if self.bot.guilds_data.get(str(m.guild.id)).get("hidden") is True:
            return True
        '''
        # チャンネル設定
        # ユーザー設定
        '''

    async def fetch_msg_with_id(self, msg_guild, msg_channel_id, msg_id):
        channel = msg_guild.get_channel(msg_channel_id)
        try:
            msg = await channel.fetch_message(msg_id)
        except Exception:
            return
        return msg

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
            files = []
            embed_em = await libs.embed.Embed_ctrl.compose_embed(self.bot, msg, message)
            await message.channel.send(embed=embed_em[0])
            if len(msg.attachments) >= 2:
                # atm_em = attachment_embed
                msg.attachments.pop(0)
                for attachment in msg.attachments:
                    atm_em = Embed()
                    atm_em.set_image(
                        url=attachment.proxy_url
                    )
                    await message.channel.send(embed=atm_em)
            for embed in msg.embeds:
                await message.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Expand(bot))
