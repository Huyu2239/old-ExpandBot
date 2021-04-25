import json


class Database:
    async def get_all_data(bot):
        mute_data = await Database.get_mute_data()
        return mute_data

    async def write_all_data(bot):
        await Database.write_mute_data()

    async def get_mute_data(bot):
        with open(f'{bot.data_directory}mute_data.json') as f:
            bot.mute_data = json.load(f)

    async def write_mute_data(bot):
        with open(f'{bot.data_directory}mute_data.json', 'w', encoding='utf-8') as f:
            json.dump(bot.mute_data, f, ensure_ascii=False, indent=4)
