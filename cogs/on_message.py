import re

import discord
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

    async def find_msgs(self, message):
        msgs = list()
        message_text = re.sub(r"\|\|[^|]+?\|\|", "", message.content)
        for ids in re.finditer(regex_discord_message_url, message_text):
            if self.bot.get_guild(int(ids['guild'])) is None:
                continue
            msg = await self.fetch_msg_with_id(
                msg_guild=self.bot.get_guild(int(ids['guild'])),
                msg_channel_id=int(ids['channel']),
                msg_id=int(ids['message']),
            )
            if msg is None:
                continue
            if await self.bot.check.check_mute(self.bot.mute_data, message):
                msg_allow = await self.bot.check.check_allow(self.bot, msg, message)
                if msg_allow is False:
                    continue
            if message.guild.id != int(ids['guild']):
                msg_hidden = await self.bot.check.check_hidden(self.bot, msg)
                if msg_hidden is True:
                    msg_allow = await self.bot.check.check_allow(self.bot, message, msg)
                    if msg_allow is False:
                        continue
            msgs.append(msg)
        if len(msgs) != len(re.findall(regex_discord_message_url, message_text)):
            await message.add_reaction('\U0000274c')
        return msgs

    async def fetch_msg_with_id(self, msg_guild, msg_channel_id, msg_id):
        channel = msg_guild.get_channel(msg_channel_id)
        if channel is None:
            return
        try:
            msg = await channel.fetch_message(msg_id)
        except Exception:
            return
        return msg

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or message.guild is None:
            return
        msgs = await self.find_msgs(message)
        if msgs is None:
            return
        for msg in msgs:
            sent_emsgs = []
            embed_em = await self.bot.embed.compose_embed(self.bot, msg, message)
            sent_emsgs.append(await message.channel.send(embed=embed_em[0]))
            if len(msg.attachments) >= 2:
                for attachment in msg.attachments[1:]:
                    embed = discord.Embed()
                    embed.set_image(
                        url=attachment.proxy_url
                    )
                    sent_emsgs.append(await message.channel.send(embed=embed))

            for embed in msg.embeds:
                sent_emsgs.append(await message.channel.send(embed=embed))

            main_message = sent_emsgs.pop(0)
            main_embed = main_message.embeds[0]
            extra_messages = ",".join([str(emsg.id) for emsg in sent_emsgs])
            url = "{0.jump_url}?base_aid={1.id}&aid={2.id}&extra={3}".format(
                message, message.author, msg.author, extra_messages)
            if url.endswith('='):
                url += '0'
            main_embed.set_author(
                name=main_embed.author.name,
                icon_url=main_embed.author.icon_url,
                url=url
            )
            await main_message.edit(embed=main_embed)


def setup(bot):
    bot.add_cog(Expand(bot))
