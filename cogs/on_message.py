import re

import discord
from discord.ext import commands
import asyncio

regex_discord_message_url = (
    'https://(ptb.|canary.)?discord(app)?.com/channels/'
    '(?P<guild>[0-9]{18})/(?P<channel>[0-9]{18})/(?P<message>[0-9]{18})'
)


class Expand(commands.Cog):
    '''
    message: on_messageの引数によるMessageObject
    msg(msgs): 引用されたMessageObject
    m :botが送信したMessageObject
    Check.hoge: 当てはまる時にTrue
    '''
    def __init__(self, bot):
        self.bot = bot

    async def find_msgs(self, message):
        msgs = list()
        error = list()
        message_text = re.sub(r"\|\|[^|]+?\|\|", "", message.content)
        urls = re.findall(regex_discord_message_url, message_text)
        for url in urls:
            ids = re.match(regex_discord_message_url, url)
            if self.bot.get_guild(int(ids['guild'])) is None:
                error.append({'url': url, 'content': 'GuildNotFound'})
                continue
            msg = await self.fetch_msg_with_id(
                msg_guild=self.bot.get_guild(int(ids['guild'])),
                msg_channel_id=int(ids['channel']),
                msg_id=int(ids['message']),
                error=error
            )
            if isinstance(msg, str):
                error.append({'url': url, 'content': msg})
                continue
            if message.guild.id != int(ids['guild']):
                msg_allow = await self.bot.Check.allow(self.bot, message, msg)
                if msg_allow is False:
                    error.append({'url': url, 'content': 'NotAllowded'})
                    continue
                msg_hidden = await self.bot.Check.hidden(self.bot, msg)
                if msg_hidden is True:
                    error.append({'url': url, 'content': 'HiddenMessage'})
                    continue
            msgs.append(msg)
        return msgs, error

    async def fetch_msg_with_id(self, msg_guild, msg_channel_id, msg_id):
        channel = msg_guild.get_channel(msg_channel_id)
        if channel is None:
            return 'ChannelNotFound'
        try:
            msg = await channel.fetch_message(msg_id)
        except Exception:
            return 'MessageNotFound'
        return msg

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or message.guild is None:
            return
        if await self.bot.Check.mute(self.bot.mute_data, message):
            return
        msgs, error = await self.find_msgs(message)
        for msg in msgs:
            sent_ms = []
            embed_em = await self.bot.embed.compose_embed(self.bot, msg, message)
            sent_ms.append(await message.channel.send(embed=embed_em[0]))
            if len(msg.attachments) >= 2:
                for attachment in msg.attachments[1:]:
                    embed = discord.Embed()
                    embed.set_image(
                        url=attachment.proxy_url
                    )
                    sent_ms.append(await message.channel.send(embed=embed))

            for embed in msg.embeds:
                sent_ms.append(await message.channel.send(embed=embed))

            main_message = sent_ms.pop(0)
            main_embed = main_message.embeds[0]
            extra_messages = ",".join([str(emsg.id) for emsg in sent_ms])
            url = f'{main_embed.author.url}?{extra_messages}'
            main_embed.set_author(
                name=main_embed.author.name,
                icon_url=main_embed.author.icon_url,
                url=url
            )
            await main_message.edit(embed=main_embed)
        if not error:
            return

        def reaction_check(reaction, user):
            if reaction.message.id == message.id:
                return True

        await message.add_reaction('\U0000274c')
        try:
            self.bot.wait_for('reaction', timeout=30, check=reaction_check)
        except asyncio.TimeoutError:
            return await message.remove_reaction('\U0000274c')
        embed = discord.Embed(title='ERROR', colour=discord.colour.red())
        for e in error:
            embed.add_field(
                name=e.get('content'),
                value=e.get('url')
            )
        await message.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Expand(bot))
