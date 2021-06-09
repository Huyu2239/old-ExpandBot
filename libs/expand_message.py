class ExpandMessage:
    def __init__(self, message):
        self.guild_config = GuildConfig(message.guild.id)
        self.member_config = self.guild_config.MemberConfig(message.author.id)
        self.user_config = UserConfig(message.author.id)

        if self.member_config:
            self.config = self.member_config
        elif self.user_config:
            self.config = self.user_config
        elif self.guild_config:
            self.config = self.guild_config
        else:
            self.config = None  # ここでエラー起こしたい

    def allow_to_be_quoted_by(self, send_message):
        num = 1
        send_message_data_list = [
            send_message.guild.id,
            send_message.channel.category_id,
            send_message.channel.id,
            send_message.author.id
        ] + [role.id for role in send_message.author.roles]
        # guild
        if self.guild_config:
            valid_elements = set(send_message_data_list) & set(self.guild_config.allow)
            num *= (-1)**len(valid_elements)
        # member
        if self.member_config:
            valid_elements = set(send_message_data_list) & set(self.member_config.allow)
            num *= (-1)**len(valid_elements)
        # user
        if self.user_config:
            valid_elements = set(send_message_data_list) & set(self.user_config.allow)
            num *= (-1)**len(valid_elements)

        if num == -1:
            return True  # 奇数だったら有効
        else:
            return False  # 偶数だったら無効
    
    def is_hidden(self):
        return self.config.hidden

    def is_anonymous(self):
        return self.config.anonymous

    def embed_type(self):
        return self.config.embed_type

    def embed_color(self):
        return self.config.embed_color
