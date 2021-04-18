from discord import Embed
import os
import json

if os.name == 'nt':
    data_directory = 'json\\'
else:
    data_directory = 'json/'


async def get_embed_type(guild_id):
    with open(f'{data_directory}guilds_data.json') as f:
        json_dict = json.load(f)
    guild_data = json_dict.get(str(guild_id))
    if guild_data is None:
        return 1
    embed_type = guild_data.get('em_type')
    if embed_type is None:
        return 1
    return embed_type


async def compose_embed(message, guild_id):
    embed_type = await get_embed_type(guild_id)
    embed = ''
    if embed_type == 1:
        embed = await compose_1(message)
    return embed, embed_type


async def compose_1(message):
    embed = Embed(
        description=message.content,
        timestamp=message.created_at,
    )
    embed.set_author(
        name=message.author.display_name,
        icon_url=message.author.avatar_url,
    )
    embed.set_footer(
        text=f'{message.guild.name}|{message.channel.name}|',
        icon_url=message.guild.icon_url,
    )
    if message.attachments and message.attachments[0].proxy_url:
        embed.set_image(
            url=message.attachments[0].proxy_url
        )
    return embed
