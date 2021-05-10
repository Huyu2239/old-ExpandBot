async def check_mute(mute_data, message):
    num = 1
    if message.guild.id in mute_data.get('guilds'):
        num *= -1
    '''
    if message.category:
        if message.category.id in mute_data.get('categories'):
            num *= -1
    '''
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

async def check_hidden(m):
    # サーバー設定
    guild_data = self.guilds_data.get(str(m.guild.id))
    if guild_data:
        if guild.data.get('hidden') is True:
            return True
    '''
    # チャンネル設定
    # ユーザー設定
    '''

async def check_anonymity(msg):
    pass