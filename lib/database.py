import json


class Database:
    def __init__(self, bot):
        self.bot = bot

    async def get_all_data(self):
        mute_data = await self.get_mute_data()
        return mute_data

    async def write_all_data(self):
        await self.write_mute_data()

    async def get_mute_data(self):
        with open(f'{self.bot.data_directory}mute_data.json') as f:
            self.bot.mute_data = json.load(f)

    async def write_mute_data(self):
        with open(f'{self.bot.data_directory}mute_data.json', 'w', encoding='utf-8') as f:
            json.dump(self.bot.mute_data, f, ensure_ascii=False, indent=4)
