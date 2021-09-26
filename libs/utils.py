from .dataaccess import MuteConfigs
from .enums import MutingTarget


async def muted_in(message):
    num = 1
    if await MuteConfigs.read(message.author.id, MutingTarget.USER):
        num *= -1
    if await MuteConfigs.read(message.guild.id, MutingTarget.GUILD):
        num *= -1
    if message.channel.category:
        if await MuteConfigs.read(message.channel.category_id, MutingTarget.CATEGORY):
            num *= -1
    if await MuteConfigs.read(message.channel.id, MutingTarget.CHANNEL):
        num *= -1
    for role in message.author.roles:
        if await MuteConfigs.read(role.id, MutingTarget.ROLE):
            num *= -1
    return num == -1
