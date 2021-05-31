class Check:
    async def com_per(ctx, target):
        if target == 1:
            if ctx.guild is None:
                await ctx.send('ユーザー設定以外はDMで実行できません。')
                return False
            if not ctx.author.guild_permissions.manage_guild:
                await ctx.send()
                return False
        return True

    async def mute(mute_data, message):
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

    async def hidden(bot, m):
        # users
        user_data = bot.users_data.get(str(m.author.id))
        if user_data:
            return user_data.get('hidden')
        # guilds
        guild_data = bot.guilds_data.get(str(m.guild.id))
        if guild_data:
            return guild_data.get('hidden')
        return True

    async def anonymity(target_data, target_id):
        target_dict = target_data.get(str(target_id))
        if target_dict:
            return target_dict.get('anonymity')
        else:
            return None

    async def allow(bot, message, msg):
        num = 1
        message_data_list = [message.guild.id, message.channel.category_id, message.channel.id, message.author.id] + [role.id for role in message.author.roles]
        # guild
        msg_guild_data = bot.guilds_data.get(str(msg.guild.id))
        if msg_guild_data:
            valid_elements = set(message_data_list) & set(msg_guild_data.get('allow'))
            num *= (-1)**len(valid_elements)
        # user
        msg_user_data = bot.users_data.get(str(msg.author.id))
        if msg_user_data:
            valid_elements = set(message_data_list) & set(msg_user_data.get('allow'))
            num *= (-1)**len(valid_elements)

        if num == -1:
            return True
        else:
            return False
