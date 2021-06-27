import asyncio
import re

import discord
from discord.ext import commands

regex_discord_message_url = (
    "https://(ptb.|canary.)?discord(app)?.com/channels/"
    "(?P<guild>[0-9]{18})/(?P<channel>[0-9]{18})/(?P<message>[0-9]{18})"
)
EMOJI_ERROR_UNQUOTABLE = "\U0000274c"


class FetchMessageResult:
    def __init__(self, is_success, msg, url, error):
        self.is_success = is_success
        self.msg = msg
        self.url = url
        self.error = error


class Expand(commands.Cog):
    """
    message: on_messageの引数によるMessageObject
    msg(msgs): 引用されたMessageObject
    m :botが送信したMessageObject
    Check.hoge: 当てはまる時にTrue
    """

    def __init__(self, bot):
        self.bot = bot

    async def find_msgs(self, message):
        results: list[FetchMessageResult] = []
        message_text = re.sub(r"\|\|[^|]+?\|\|", "", message.content)
        for url_mutch in re.finditer(regex_discord_message_url, message_text):
            ids = url_mutch.groupdict()
            url = url_mutch[0]
            if self.bot.get_guild(int(ids["guild"])) is None:
                results.append(FetchMessageResult(False, None, url, "Guild-NotFound"))
                continue
            msg, error = await self.fetch_msg_with_id(
                msg_guild=self.bot.get_guild(int(ids["guild"])),
                msg_channel_id=int(ids["channel"]),
                msg_id=int(ids["message"]),
            )
            if error:
                results.append(FetchMessageResult(False, None, url, error))
                continue
            if message.guild.id != int(ids["guild"]):
                msg_allow = await self.bot.Check.allow(self.bot, message, msg)
                if msg_allow is False:
                    results.append(FetchMessageResult(False, None, url, "NotAllowed"))
                    continue
                msg_hidden = await self.bot.Check.hidden(self.bot, msg)
                if msg_hidden is True:
                    results.append(
                        FetchMessageResult(False, None, url, "HiddenMessage")
                    )
                    continue
            results.append(FetchMessageResult(True, msg, url, None))
        return results

    async def fetch_msg_with_id(self, msg_guild, msg_channel_id, msg_id):
        channel = msg_guild.get_channel(msg_channel_id)
        if channel is None:
            return None, "Channel-NotFound"
        try:
            msg = await channel.fetch_message(msg_id)
        except Exception:
            return None, "Message-NotFound"
        return msg, None

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or message.guild is None:
            return
        if await self.bot.get_cog("Mute").muted_in(message):
            return
        results = await self.find_msgs(message)
        errors = []
        for result in results:
            if not result.is_success:
                errors.append(result)
                continue
            msg = result.msg
            sent_ms = []
            embed_em = await self.bot.embed.compose_embed(self.bot, msg, message)
            sent_ms.append(await message.channel.send(embed=embed_em[0]))
            if len(msg.attachments) >= 2:
                for attachment in msg.attachments[1:]:
                    embed = discord.Embed()
                    embed.set_image(url=attachment.proxy_url)
                    sent_ms.append(await message.channel.send(embed=embed))

            for embed in msg.embeds:
                sent_ms.append(await message.channel.send(embed=embed))

            main_message = sent_ms.pop(0)
            main_embed = main_message.embeds[0]
            extra_messages = ",".join([str(emsg.id) for emsg in sent_ms])
            url = f"{main_embed.author.url}?{extra_messages}"
            main_embed.set_author(
                name=main_embed.author.name,
                icon_url=main_embed.author.icon_url,
                url=url,
            )
            await main_message.edit(embed=main_embed)
        if not errors:
            return

        def reaction_check(reaction, user):
            if (
                user.bot
                or reaction.message.id != message.id
                and str(reaction.emoji) != EMOJI_ERROR_UNQUOTABLE
            ):
                return False
            return True

        await message.add_reaction(EMOJI_ERROR_UNQUOTABLE)
        try:
            await self.bot.wait_for("reaction_add", timeout=15, check=reaction_check)
        except asyncio.TimeoutError:
            return await message.remove_reaction(
                EMOJI_ERROR_UNQUOTABLE, member=message.guild.me
            )
        embed = discord.Embed(title="ERROR", colour=discord.Color.red())
        for e in errors:
            embed.add_field(name=e.error, value=e.url)
        await message.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Expand(bot))
