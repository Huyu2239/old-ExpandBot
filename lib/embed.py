from discord import Embed
import os

if os.name == 'nt':
    data_directory = 'json\\'
else:
    data_directory = 'json/'


class Embed_ctrl:
    def __init__(self):
        return

    async def compose_embed(self, msg, message):
        names = self.get_names(msg, message)
        embed_type = await self.get_embed_type(self, message.guild.id)
        embed = ''
        if embed_type == 1:
            embed = await self.compose_1(msg, message, names)
        return embed, embed_type

    async def get_names(self, msg, message):
        '''
        names = {}
        '''
        names = {
            "user_name": msg.author.display_name,
            "user_icon": msg.author.avatar_url,
            "channel_name": msg.channel.name,
            "guild_name": msg.guild.name,
            "guild_icon": msg.guild.icon_url
        }
        return names

    async def get_embed_type(self, guild_id):
        guild_data = self.bot.guilds_data.get(str(guild_id))
        if guild_data is None:
            return 1
        embed_type = guild_data.get('em_type')
        if embed_type is None:
            return 1
        return embed_type

    async def compose_1(self, msg, message, names):
        embed = Embed(
            description=msg.content,
            timestamp=msg.created_at,
        )
        embed.set_author(
            name=names["user_name"],
            icon_url=names["guild_icon"]
        )
        embed.set_footer(
            text=f'Quoted by <@{message.author.id}>\n{names["guild_name"]}|{names["channel_name"]}|',
            icon_url=names["guild_icon"],
        )
        if msg.attachments and msg.attachments[0].proxy_url:
            embed.set_image(
                url=msg.attachments[0].proxy_url
            )
        return embed
