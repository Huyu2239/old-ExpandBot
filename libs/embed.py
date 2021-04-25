from discord import Embed
import os

if os.name == 'nt':
    data_directory = 'json\\'
else:
    data_directory = 'json/'


class Embed_ctrl:
    async def compose_embed(bot, msg, message):
        embed = ''
        names = await Embed_ctrl.get_names(bot, msg, message)
        embed_type = await Embed_ctrl.get_embed_type(bot, message.guild.id)
        if embed_type == 1:
            embed = await Embed_ctrl.compose_1(msg, message, names)
        return embed, embed_type

    async def get_names(bot, msg, message):
        names = {
            "user_name": msg.author.display_name,
            "user_icon": msg.author.avatar_url,
            "channel_name": msg.channel.name,
            "guild_name": msg.guild.name,
            "guild_icon": msg.guild.icon_url
        }
        '''
        if self.bot.users_data.get(str(msg.author.id)):
            if self.bot.users_data.get(str(msg.author.id)).get('') is True:
                names["user_name] = '匿名ユーザー'
                names["user_icon"] = "初期アイコン"
        if self.bot.channels_data.get(str(msg.channel.id)):
            if self.bot.channels_data.get(str(msg.channel.id)).get('') is True:
                names["channel_name"] = '匿名チャンネル'
        if self.bot.guilds_data.get(str(msg.guild.id)):
            ifself.bot.guilds_data.get(str(msg.guild.id)).get('') is True:
                names["guild_name"] = '匿名サーバー'
                names['guild_icon'] = 初期アイコン
        '''
        return names

    async def get_embed_type(bot, guild_id):
        guild_data = bot.guilds_data.get(str(guild_id))
        if guild_data is None:
            return 1
        embed_type = guild_data.get('em_type')
        if embed_type is None:
            return 1
        return embed_type

    async def compose_1(msg, message, names):
        embed = Embed(
            description=msg.content,
            timestamp=msg.created_at,
        )
        embed.set_author(
            name=names["user_name"],
            icon_url=names["user_icon"]
        )
        embed.set_footer(
            text=f'@{names["guild_name"]} | #{names["channel_name"]} | Quoted by {str(message.author)}',
            icon_url=names["guild_icon"],
        )
        if msg.attachments and msg.attachments[0].proxy_url:
            embed.set_image(
                url=msg.attachments[0].proxy_url
            )
        return embed
