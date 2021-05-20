async def check_com_per(ctx, target):
    if target != 5:
        if ctx.guild is None:
            await ctx.send('ユーザー設定以外はDMで実行できません。')
            return False
        if not ctx.author.guild_permissions.manage_guild:
            await ctx.send()
            return False
    return True


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
        return user_data.get('hidden')
    # roles
    for role in m.author.roles:
        role_data = bot.roles_data.get(str(role.id))
        if role_data:
            return role_data.get('hidden')
    # channels
    channel_data = bot.channels_data.get(str(m.channel.id))
    if channel_data:
        return channel_data.get('hidden')
    # categories
    if m.channel.category:
        category_data = bot.categories_data.get(str(m.channel.category_id))
        if category_data:
            return category_data.get('hidden')
    # guilds
    guild_data = bot.guilds_data.get(str(m.guild.id))
    if guild_data:
        return guild_data.get('hidden')
    return False


async def check_anonymity(target_data, target_id):
    target_dict = target_data.get(str(target_id))
    if target_dict:
        return target_dict.get('anonymity')
    else:
        return True


async def check_allow(bot, message, msg):
    num = 1
    message_data_list = [message.guild.id, message.channel.category_id, message.channel.id, message.author.id] + [role.id for role in message.author.roles]
    # guild
    msg_guild_data = bot.guilds_data.get(str(msg.guild.id))
    if msg_guild_data:
        valid_elements = set(message_data_list) & set(msg_guild_data.get('allow'))
        num *= (-1)**len(valid_elements)
    # category
    msg_categories_data = bot.categories_data.get(str(msg.channel.category_id))
    if msg_categories_data:
        valid_elements = set(message_data_list) & set(msg_categories_data.get('allow'))
        num *= (-1)**len(valid_elements)
    # channel
    msg_channel_data = bot.channels_data.get(str(msg.channel.id))
    if msg_channel_data:
        valid_elements = set(message_data_list) & set(msg_channel_data.get('allow'))
        num *= (-1)**len(valid_elements)
    # role
    for role in msg.author.roles:
        msg_role_data = bot.roles_data.get(str(role.id))
        if msg_role_data:
            valid_elements = set(message_data_list) & set(msg_role_data.get('allow'))
            num *= (-1)**len(valid_elements)
    # user
    msg_user_data = bot.users_data.get(str(msg.author.id))
    if msg_user_data:
        valid_elements = set(message_data_list) & set(msg_user_data.get('allow'))
        num *= (-1)**len(valid_elements)
    else:
        return False

    if num == -1:
        return True
    else:
        return False
