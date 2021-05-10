async def check_mute(self, message):
    num = 1
    md = self.bot.mute_data
    if message.guild:
        if message.guild.id in md.get('guilds'):
            num *= -1
    if message.channel.id in md.get('channels'):
        num *= -1
    for role in message.author.roles:
        if role.id in md.get('roles'):
            num *= -1
    if message.author.id in md.get('users'):
        num *= -1
    if num == -1:
        return True
    else:
        return False

async def check_hidden(self, m):
    # サーバー設定
    guild_data = self.guilds_data.get(str(m.guild.id))
    if guild_data:
        if guild.data.get('hidden') is True:
            return True
    '''
    # チャンネル設定
    # ユーザー設定
    '''

async def check_anonymity(self, msg):
    pass