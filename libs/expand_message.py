from .dataaccess import UserConfigs, MemberConfigs, GuildConfigs


class ExpandMessage:
    def __init__(self, message):
        self.member_config = MemberConfigs.read(message.author.id, message.guild.id)
        self.user_config = UserConfigs.read(message.author.id)
        self.guild_config = GuildConfigs.read(message.guild.id)
        self.config = self.member_config or self.user_config or self.guild_config or None
        if self.config is None:
            pass

    def allows_to_be_quoted_by(self, posted_message):
        num = 1
        posted_message_data_list = [
            posted_message.guild.id,
            posted_message.channel.category_id,
            posted_message.channel.id,
            posted_message.author.id,
        ] + [role.id for role in posted_message.author.roles]

        # guild
        if self.guild_config:
            valid_elements = set(posted_message_data_list) & set(
                self.guild_config.allow
            )
            num *= (-1) ** len(valid_elements)
        # member
        if self.member_config:
            valid_elements = set(posted_message_data_list) & set(
                self.member_config.allow
            )
            num *= (-1) ** len(valid_elements)
        # user
        if self.user_config:
            valid_elements = set(posted_message_data_list) & set(self.user_config.allow)
            num *= (-1) ** len(valid_elements)

        return num == -1  # 奇数で有効

    @property
    def is_hidden(self):
        return self.config.hidden

    @property
    def exceptions(self):
        return self.config.exceptions.split(",")

    @property
    def layout(self):
        return self.config.layout

    @property
    def color(self):
        return self.config.color
