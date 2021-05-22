from discord.ext import commands
import re

regex_discord_message_url = (
    '(?!<)https://(ptb.|canary.)?discord(app)?.com/channels/'
    '(?P<guild>[0-9]{18})/(?P<channel>[0-9]{18})/(?P<message>[0-9]{18})(?!>)'
)
regex_extra_url = (
    r'\?base_aid=(?P<base_author_id>[0-9]{18})'
    '&aid=(?P<author_id>[0-9]{18})'
    '&extra=(?P<extra_messages>[0-9,]+)'
)


class Del(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def from_jump_url(self, url):
        print(url)
        base_url_match = re.match(regex_discord_message_url + regex_extra_url, url)
        data = base_url_match.groupdict()
        return {
            "base_author_id": int(data["base_author_id"]),
            "author_id": int(data["author_id"]),
            "extra_messages": [int(_id) for _id in data["extra_messages"].split(",")]
        }

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.member.bot or str(payload.emoji) == '\U0001f5d1':
            return
        msg = await (self.bot.get_channel(payload.channel_id)).fetch_message(payload.message_id)
        if msg.author.id != self.bot.user.id or not msg.embeds:
            return

        target_embed = msg.embeds[0]
        if getattr(target_embed.author, "url", None) is None:
            return
        data = await self.from_jump_url(target_embed.author.url)
        if not (data["base_author_id"] == payload.member.id or data["author_id"] == payload.member.id):
            return
        await msg.delete()
        if data["extra_messages"] == '0':
            return
        for message_id in data["extra_messages"]:
            extra_message = await msg.channel.fetch_message(message_id)
            if extra_message is not None:
                await extra_message.delete()


def setup(bot):
    bot.add_cog(Del(bot))
