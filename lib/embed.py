from discord import Embed
import os
import json

if os.name == 'nt':
    data_directory = 'json\\'
else:
    data_directory = 'json/'


async def compose_embed(message, guild_id):
    embed_type = await get_embed_type(guild_id)
    if embed_type == 1:
        return compose_1(message)


async def get_embed_type(guild_id):
    with open(f'{data_directory}embed_type.json') as f:
        json_dict = json.load(f)
    num = 0
    while num < 3:
        num += 1
        if guild_id in json_dict.get(str(num)):
            break
    return num


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
        text=message.channel.name,
        icon_url=message.guild.icon_url,
    )
    if message.attachments and message.attachments[0].proxy_url:
        embed.set_image(
            url=message.attachments[0].proxy_url
        )
    return embed
