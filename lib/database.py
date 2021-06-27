import json


async def write_new_config(target_dict: dict, target_id):
    tmp_dict = {
        'hidden': True,
        'anonymity': True,
        'embed_type': 1,
        'embed_color': '000000',
        'allow': []
    }
    target_dict[str(target_id)] = tmp_dict
    return target_dict.get(str(target_id))


async def read_all_configs(bot):
    mute_configs = await MuteConfigs.read(bot)
    guild_configs = await GuildConfigs.read(bot)
    user_configs = await UserConfigs.read(bot)
    return mute_configs, guild_configs, user_configs


async def write_all_configs(bot):
    await MuteConfigs.write(bot)
    await GuildConfigs.write(bot)
    await UserConfigs.write(bot)


class MuteConfigs:
    async def read(bot):
        with open(f'{bot.data_directory}mute_configs.json') as f:
            bot.get_cog("Mute").mute_configs = json.load(f)

    async def write(bot):
        with open(f'{bot.data_directory}mute_configs.json', 'w', encoding='utf-8') as f:
            json.dump(bot.get_cog("Mute").mute_configs, f, ensure_ascii=False, indent=4)


class GuildConfigs:
    async def read(bot):
        with open(f'{bot.data_directory}guild_configs.json') as f:
            bot.guild_configs = json.load(f)

    async def write(bot):
        with open(f'{bot.data_directory}guild_configs.json', 'w', encoding='utf-8') as f:
            json.dump(bot.guild_configs, f, ensure_ascii=False, indent=4)


class UserConfigs:
    async def read(bot):
        with open(f'{bot.data_directory}user_configs.json') as f:
            bot.user_configs = json.load(f)

    async def write(bot):
        with open(f'{bot.data_directory}user_configs.json', 'w', encoding='utf-8') as f:
            json.dump(bot.user_configs, f, ensure_ascii=False, indent=4)
