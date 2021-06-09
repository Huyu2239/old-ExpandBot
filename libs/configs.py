guild_configs = {}
user_configs = {}

def set_config_elements(self, config):
    """カプセル化"""
    self.hidden = config.get('hidden')
    self.anonymous = config.get('anonymous')
    self.embed_type = config.get('embed_type')
    self.embed_color = config.get('embed_color')
    self.allow = config.get('allow')

def edit_config_elements(target_config, target_element, value=None):
    """setコマンドによるelementのedit関数"""
    pass

class GuildConfig:
    def __init__(self, guild_id):
        guild_config = guilds_configs.get(str(guild_id))
        set_config(self, guild_config)

    class MemberConfig:
        def __init__(self, member_id):
            if guild_config is None:
                return
            member_config = guild_config.get(str(member_id))
            set_config(self, member_config)


class UserConfig:
    def __init__(serl, user_id):
        user_config = user_configs.get(str(user_id))
        set_config(self, user_config)
