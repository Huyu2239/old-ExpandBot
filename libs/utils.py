import discord
from .dataaccess import MuteConfigs
from .enums import MutingTargets


async def muted_in(message):
    num = 1
    if await MuteConfigs.read(message.author.id, MutingTargets.USER):
        num *= -1
    if await MuteConfigs.read(message.guild.id, MutingTargets.GUILD):
        num *= -1
    if message.channel.category:
        if await MuteConfigs.read(message.channel.category_id, MutingTargets.CATEGORY):
            num *= -1
    if await MuteConfigs.read(message.channel.id, MutingTargets.CHANNEL):
        num *= -1
    for role in message.author.roles:
        if await MuteConfigs.read(role.id, MutingTargets.ROLE):
            num *= -1
    return num == -1


def convert_to_emoji_from_bool(target_bool):
    if target_bool is True:
        return "<:True:850591234283798558>"
    elif target_bool is False:
        return "<:False:850591522171912202>"
    else:
        return "<:None:850591553688436746>"


async def compose_embeds(msg, message):
    embed = discord.Embed(
        description=msg.content,
        timestamp=msg.created_at,
        url=f'{message.jump_url}?{message.author.id}',
        colour=int(f'0x{embed_color}', 16)
    )
    embed.set_author(
        name=msg.author.display_name,
        icon_url=msg.author.avatar_url,
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
