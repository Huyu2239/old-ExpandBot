from discord import Embed


async def compose_embed(bot, msg, message):
    names = await get_names(bot, msg, message)
    embed_type = await get_embed_type(bot, message)
    if embed_type == 1:
        embed = await Compose.type_1(msg, message, names)
    else:
        embed = await Compose.type_1(msg, message, names)
    return embed, embed_type

async def get_names(bot, msg, message):
    names = {
        "user_name": msg.author.display_name,
        "user_icon": msg.author.avatar_url,
        "channel_name": msg.channel.name,
        "guild_name": msg.guild.name,
        "guild_icon": msg.guild.icon_url
    }
    if msg.channel.category:
        names["category_name"] = msg.channel.category.name

    if await bot.check.check_anonymity(bot.users_data, msg.author.id):
        names["user_name"] = '匿名ユーザー'
        names["user_icon"] = 'https://cdn.discordapp.com/embed/avatars/0.png'
    if await bot.check.check_anonymity(bot.channels_data, msg.channel.id):
        names["channel_name"] = '匿名チャンネル'
    if await bot.check.check_anonymity(bot.categories_data, msg.channel.category_id):
        names["category_name"] = '匿名カテゴリ'
    if await bot.check.check_anonymity(bot.guilds_data, msg.guild.id):
        names["guild_name"] = '匿名サーバー'
        names["guild_icon"] = 'https://cdn.discordapp.com/embed/avatars/0.png'
    return names

async def get_embed_type(bot, message):
    user_data = bot.users_data.get(str(message.author.id))
    if user_data:
        return user_data.get('embed_type')
    '''
    role
    '''
    channel_data = bot.channels_data.get(str(message.channel.id))
    if channel_data:
        return channel_data.get('embed_type')
    if message.channel.category:
        category_data = bot.categories_data.get(str(message.channel.category_id))
        if channel_data:
            return channel_data.get('embed_type')
    guild_data = bot.guilds_data.get(str(message.guild.id))
    if guild_data:
        return guild_data.get('embed_type')
    return 1

class Compose:
    async def type_1(msg, message, names):
        embed = Embed(
            description=msg.content,
            timestamp=msg.created_at,
        )
        embed.set_author(
            name=names["user_name"],
            icon_url=names["user_icon"]
        )
        if names.get('category_name') is None:
            channel_txt = f'#{names["channel_name"]}'
        else:
            channel_txt = f'#{names["category_name"]}/{names["channel_name"]}'
        if msg.guild == message.guild:
            footer_txt = f'{channel_txt} | Quoted by {str(message.author)}'
        else:
            footer_txt = f'@{names["guild_name"]} | {channel_txt} | Quoted by {str(message.author)}'
        embed.set_footer(
            text=footer_txt,
            icon_url=names["guild_icon"],
        )
        if msg.attachments and msg.attachments[0].proxy_url:
            embed.set_image(
                url=msg.attachments[0].proxy_url
            )
        return embed
