from .configs import *

class ExpandMessage:
    """ExpandBotで扱うメッセージオブジェクト　引用者と被引用者どちらでも使うつもり"""
    def __init__(self, message):
        self.guild_config = GuildConfig(message.guild.id)
        self.member_config = self.guild_config.MemberConfig(message.author.id)
        self.user_config = UserConfig(message.author.id)

        # 存在していて、かつ優先順位が最高のものを self.config に代入
        if self.member_config:
            self.config = self.member_config
        elif self.user_config:
            self.config = self.user_config
        elif self.guild_config:
            self.config = self.guild_config
        else:
            self.config = None  # ここでエラー起こしたい

    def allows_quoting_by(self, sent_message):
        num = 1
        sent_message_data_list = [
            sent_message.guild.id,
            sent_message.channel.category_id,
            sent_message.channel.id,
            sent_message.author.id
        ] + [role.id for role in sent_message.author.roles]

        # guild
        if self.guild_config:
            valid_elements = set(sent_message_data_list) & set(self.guild_config.allow)
            num *= (-1)**len(valid_elements)
        # member
        if self.member_config:
            valid_elements = set(sent_message_data_list) & set(self.member_config.allow)
            num *= (-1)**len(valid_elements)
        # user
        if self.user_config:
            valid_elements = set(sent_message_data_list) & set(self.user_config.allow)
            num *= (-1)**len(valid_elements)

        return num == -1  # 奇数で有効
    
    @property
    def is_hidden(self):
        return self.config.hidden

    @property
    def is_anonymous(self):
        return self.config.anonymous

    @property
    def embed_type(self):
        return self.config.embed_type

    @property
    def embed_color(self):
        return self.config.embed_color
