from discord.ext import commands

EMOJI_DELETE_UNQUOTABLE = "\U0001f5d1"


class DeleteMessageByReaction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_data_with_embed(self, target_embed):
        message_list = target_embed.url.split("?")
        msg_list = target_embed.author.url.split("?")
        data = {"base_author_id": int(message_list[1]), "author_id": int(msg_list[1])}
        if len(msg_list) == 3:
            data["extra_messages"] = [int(_id) for _id in msg_list[2].split(",")]
        return data

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.member.bot or str(payload.emoji) != EMOJI_DELETE_UNQUOTABLE:
            return
        msg = await (self.bot.get_channel(payload.channel_id)).fetch_message(
            payload.message_id
        )
        if msg.author.id != self.bot.user.id or not msg.embeds:
            return

        target_embed = msg.embeds[0]
        if getattr(target_embed.author, "url", None) is None or not target_embed.url:
            return
        data = await self.get_data_with_embed(target_embed)
        if not (
            data["base_author_id"] == payload.member.id
            or data["author_id"] == payload.member.id
        ):
            return
        if data.get("extra_messages"):
            for message_id in data["extra_messages"]:
                extra_message = await msg.channel.fetch_message(message_id)
                if extra_message is not None:
                    await extra_message.delete()
        await msg.delete()


def setup(bot):
    bot.add_cog(DeleteMessageByReaction(bot))
