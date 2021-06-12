import os
import json

class DataAccess:
    def __init__(self):
        if os.name == 'nt':
            access = JsonDB()
        else:
            access = PostgreSQLDB()

        self.access = access
        self.guild_configs = access.guild_configs
        self.user_configs = access.user_configs
        self.mute_config = access.mute_config
    
    def read(self):
        return self.access.read()
    
    def write(self):
        return self.access.write()


class JsonDB:
    def __init__(self):
        self.data_directory = 'json\\'
        self.guild_configs, self.user_configs, self.mute_settings = self.read()
    
    def read(self):
        with open(f'{self.data_directory}guild_configs.json') as f:
            guild_configs = json.load(f)
        with open(f'{self.data_directory}user_configs.json') as f:
            user_configs = json.load(f)
        with open(f'{self.data_directory}mute_settings.json') as f:
            mute_settings = json.load(f)
        return guild_configs, user_configs, mute_settings

    def write(self):
        with open(f'{self.data_directory}guild_configs.json', 'w', encoding='utf-8') as f:
            json.dump(self.guild_configs, f, ensure_ascii=False, indent=4)
        with open(f'{self.data_directory}user_configs.json', 'w', encoding='utf-8') as f:
            json.dump(self.user_configs, f, ensure_ascii=False, indent=4)
        with open(f'{self.data_directory}mute_settings.json', 'w', encoding='utf-8') as f:
            json.dump(mute_settings, f, ensure_ascii=False, indent=4)


class PostgreSQLDB:
    def __init__(self):
        pass