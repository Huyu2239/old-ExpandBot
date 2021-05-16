import json


async def write_new_data(target_dict: dict, target_id):
    tmp_dict = {
        'hidden': True,
        'anonymity': True,
        'embed_type': 1,
        'embed_color': 0,
        'allow': []
    }
    target_dict[str(target_id)] = tmp_dict
    return target_dict.get(str(target_id))


async def read_all_data(bot):
    mute_data = await Mute_Data.read(bot)
    guilds_data = await Guilds_Data.read(bot)
    categories_data = await Categories_Data.read(bot)
    channels_data = await Channels_Data.read(bot)
    roles_data = await Roles_Data.read(bot)
    users_data = await Users_Data.read(bot)
    return mute_data, guilds_data, categories_data, channels_data, roles_data, users_data


async def write_all_data(bot):
    await Mute_Data.write(bot)
    await Guilds_Data.write(bot)
    await Categories_Data.write(bot)
    await Channels_Data.write(bot)
    await Roles_Data.write(bot)
    await Users_Data.write(bot)


class Mute_Data:
    async def read(bot):
        with open(f'{bot.data_directory}mute_data.json') as f:
            bot.mute_data = json.load(f)

    async def write(bot):
        with open(f'{bot.data_directory}mute_data.json', 'w', encoding='utf-8') as f:
            json.dump(bot.mute_data, f, ensure_ascii=False, indent=4)


class Guilds_Data:
    async def read(bot):
        with open(f'{bot.data_directory}guilds_data.json') as f:
            bot.guilds_data = json.load(f)

    async def write(bot):
        with open(f'{bot.data_directory}guilds_data.json', 'w', encoding='utf-8') as f:
            json.dump(bot.guilds_data, f, ensure_ascii=False, indent=4)


class Categories_Data:
    async def read(bot):
        with open(f'{bot.data_directory}categories_data.json') as f:
            bot.categories_data = json.load(f)

    async def write(bot):
        with open(f'{bot.data_directory}categories_data.json', 'w', encoding='utf-8') as f:
            json.dump(bot.categories_data, f, ensure_ascii=False, indent=4)


class Channels_Data:
    async def read(bot):
        with open(f'{bot.data_directory}channels_data.json') as f:
            bot.channels_data = json.load(f)

    async def write(bot):
        with open(f'{bot.data_directory}channels_data.json', 'w', encoding='utf-8') as f:
            json.dump(bot.channels_data, f, ensure_ascii=False, indent=4)


class Roles_Data:
    async def read(bot):
        with open(f'{bot.data_directory}roles_data.json') as f:
            bot.roles_data = json.load(f)

    async def write(bot):
        with open(f'{bot.data_directory}roles_data.json', 'w', encoding='utf-8') as f:
            json.dump(bot.roles_data, f, ensure_ascii=False, indent=4)


class Users_Data:
    async def read(bot):
        with open(f'{bot.data_directory}users_data.json') as f:
            bot.users_data = json.load(f)

    async def write(bot):
        with open(f'{bot.data_directory}users_data.json', 'w', encoding='utf-8') as f:
            json.dump(bot.users_data, f, ensure_ascii=False, indent=4)
