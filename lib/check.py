async def check_mute(mute_data, message):
    num = 1
    if message.guild.id in mute_data.get('guilds'):
        num *= -1
    if message.channel.category:
        if message.channel.category_id in mute_data.get('categories'):
            num *= -1
    if message.channel.id in mute_data.get('channels'):
        num *= -1
    for role in message.author.roles:
        if role.id in mute_data.get('roles'):
            num *= -1
    if message.author.id in mute_data.get('users'):
        num *= -1
    if num == -1:
        return True
    else:
        return False


async def check_hidden(bot, m):
    # users
    user_data = bot.users_data.get(str(m.author.id))
    if user_data:
        if user_data.get('hidden'):
            return True
    # roles
    '''
    '''
    # channels
    channel_data = bot.channels_data.get(str(m.channel.id))
    if channel_data:
        if channel_data.get('hidden'):
            return True
    # categories
    if m.channel.category:
        category_data = bot.categories_data.get(str(m.channel.category_id))
        if category_data:
            if category_data.get('hidden'):
                return True
    # guilds
    guild_data = bot.guilds_data.get(str(m.guild.id))
    if guild_data:
        if guild_data.get('hidden'):
            return True
    return False


async def check_anonymity(target_data, target_id):
    target_dict = target_data.get(str(target_id))
    if target_dict:
        return target_dict.get('anonymity')
    else:
        return False