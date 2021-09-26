import os

import discord
from discord.ext import commands
from discord_slash import SlashCommand
from dotenv import load_dotenv


class ExpandBot(commands.Bot):
    def __init__(self, command_prefix):
        allowed_mentions = discord.AllowedMentions(
            everyone=False, roles=False, users=True
        )
        intents = discord.Intents.all()
        super().__init__(
            command_prefix=command_prefix,
            intents=intents,
            allowed_mentions=allowed_mentions,
        )
        self.set_vars()
        print("loaded")

    def set_vars(self):
        self.ready = False
        self.slash_client = SlashCommand(self, sync_commands=True)
        self.log_ch_id = int(os.environ["LOG_CH_ID"])
        self.cog_folders = [
            "management",
            "commands",
            "core",
        ]

    async def on_ready(self):
        if self.ready:
            return
        self.ready = True
        for folder in self.cog_folders:
            for cog in os.listdir(f"./{folder}"):
                if cog == "__pycache__":
                    continue
                try:
                    self.load_extension(f"{folder}.{cog[:-3]}")
                except discord.ext.commands.errors.ExtensionFailed:
                    continue
        await self.change_presence(
            activity=discord.Game(name=f"/ヘルプ | {len(self.guilds)}サーバー")
        )
        print("ready")


if __name__ == "__main__":
    load_dotenv()
    bot = ExpandBot(command_prefix="e:")
    bot.run(os.environ["TOKEN"])
