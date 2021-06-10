guild_configs = {}
user_configs = {}

def set_config_elements(self, config):
    """カプセル化"""
    if config is None:
        return
    self.hidden = config.get('hidden')
    self.anonymous = config.get('anonymous')
    self.embed_type = config.get('embed_type')
    self.embed_color = config.get('embed_color')
    self.allow = config.get('allow')

def edit_config_elements(target_config, target_element, value=None):
    """setコマンドによるelementのedit関数"""
    pass

class GuildConfig:
    """Guild's Config"""
    def __init__(self, guild_id):
        guild_config = guild_configs.get(str(guild_id))
        set_config_elements(self, guild_config)

    class MemberConfig:
        """Member's Config"""
        def __init__(self, member_id):
            if GuildConfig.guild_config is None:
                return
            member_config = GuildConfig.guild_config.get(str(member_id))
            set_config_elements(self, member_config)


class UserConfig:
    """User's Config"""
    def __init__(self, user_id):
        user_config = user_configs.get(str(user_id))
        set_config_elements(self, user_config)