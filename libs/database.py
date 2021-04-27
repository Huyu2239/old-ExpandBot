import json


class Database:
    async def write_new_data(target_dict: dict, target_id):
        tmp_set = {
            'hidden': True,
            'anonimity': True,
            'embed_type': 1,
            'embed_color': 0,
            'allow': []
        }
        target_dict[str(target_id)] = tmp_set

    async def get_all_data(bot):
        mute_data = await Database.get_mute_data(bot)
        guilds_data = await Database.get_guilds_data(bot)
        return mute_data, guilds_data

    async def write_all_data(bot):
        await Database.write_mute_data(bot)
        await Database.write_guilds_data(bot)

    async def get_mute_data(bot):
        with open(f'{bot.data_directory}mute_data.json') as f:
            bot.mute_data = json.load(f)

    async def write_mute_data(bot):
        with open(f'{bot.data_directory}mute_data.json', 'w', encoding='utf-8') as f:
            json.dump(bot.mute_data, f, ensure_ascii=False, indent=4)

    async def get_guilds_data(bot):
        with open(f'{bot.data_directory}guilds_data.json') as f:
            bot.guilds_data = json.load(f)

    async def write_guilds_data(bot):
        with open(f'{bot.data_directory}guilds_data.json', 'w', encoding='utf-8') as f:
            json.dump(bot.guilds_data, f, ensure_ascii=False, indent=4)
