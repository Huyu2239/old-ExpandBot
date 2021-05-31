from discord import Embed


async def compose_embed(bot, msg, message):
    names = {
        "user_name": msg.author.display_name,
        "user_icon": msg.author.avatar_url,
        "channel_name": msg.channel.name,
        "guild_name": msg.guild.name,
        "guild_icon": msg.guild.icon_url
    }
    if msg.guild != message.guild:
        names = await update_names(bot, msg, names)
    embed_type = await get_embed_type(bot, message)
    if embed_type == 1:
        embed = await Compose.type_1(msg, message, names)
    else:
        embed = await Compose.type_1(msg, message, names)
    return embed, embed_type


async def update_names(bot, msg, names):
    guild_anonymity = await bot.check.anonymity(bot.guilds_data, msg.guild.id)
    user_anonymity = await bot.check.anonymity(bot.users_data, msg.author.id)

    if user_anonymity is None:
        if guild_anonymity:
            names["user_name"] = '匿名ユーザー'
            names["user_icon"] = 'https://discord.com/assets/7c8f476123d28d103efe381543274c25.png'
        else:
            names["user_name"] = msg.author.display_name
            names["user_icon"] = msg.author.avatar_url
    if user_anonymity is True:
        names["user_name"] = '匿名ユーザー'
        names["user_icon"] = 'https://discord.com/assets/7c8f476123d28d103efe381543274c25.png'
    if user_anonymity is False:
        names["user_name"] = msg.author.display_name
        names["user_icon"] = msg.author.avatar_url
    return names


async def get_embed_type(bot, message):
    user_data = bot.users_data.get(str(message.author.id))
    if user_data:
        return user_data.get('embed_type')
    guild_data = bot.guilds_data.get(str(message.guild.id))
    if guild_data:
        return guild_data.get('embed_type')
    return 1


class Compose:
    async def type_1(msg, message, names):
        embed = Embed(
            description=msg.content,
            timestamp=msg.created_at,
            url=f'{message.jump_url}?{message.author.id}'
        )
        embed.set_author(
            name=names["user_name"],
            icon_url=names["user_icon"],
            url=f'{msg.jump_url}?{msg.author.id}'
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
