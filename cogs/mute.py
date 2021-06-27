import asyncio
import json

import discord
from discord.ext import commands
from discord_slash import SlashContext, cog_ext
from discord_slash.utils.manage_commands import create_choice, create_option
from lib.check import MutingTargets


class Mute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        with open(f'{self.bot.data_directory}mute_configs.json') as f:
            self.mute_configs = json.load(f)
        asyncio.create_task(self.bot.slash.sync_all_commands())

    def cog_unload(self):
        self.bot.slash.remove_cog_commands(self)

    async def read(self):
        with open(f'{self.bot.data_directory}mute_configs.json') as f:
            self.mute_configs = json.load(f)

    async def write(self):
        with open(f'{self.bot.data_directory}mute_configs.json', 'w', encoding='utf-8') as f:
            json.dump(self.mute_configs, f, ensure_ascii=False, indent=4)

    async def muted_in(self, m:discord.Message):
        num = 1
        if m.guild.id in self.mute_configs.get("guilds"):
            num *= -1
        if m.channel.category:
            if m.channel.category_id in self.mute_configs.get("categories"):
                num *= -1
        if m.channel.id in self.mute_configs.get("channels"):
            num *= -1
        for role in m.author.roles:
            if role.id in self.mute_configs.get("roles"):
                num *= -1
        if m.author.id in self.mute_configs.get("users"):
            num *= -1
        return num == -1

    @cog_ext.cog_slash(
        name="mute",
        description="展開の無効化・有効化をします。",
        options=[
            create_option(
                name="target",
                description="ミュートする対象を選択",
                option_type=4,
                required=True,
                choices=[
                    create_choice(name="サーバー", value=MutingTargets.GUILD),
                    create_choice(name="カテゴリー", value=MutingTargets.CATEGORY),
                    create_choice(name="チャンネル", value=MutingTargets.CHANNEL),
                    create_choice(name="ロール", value=MutingTargets.ROLE),
                    create_choice(name="ユーザー", value=MutingTargets.USER),
                ],
            ),
            create_option(
                name="category",
                description="ミュートするカテゴリーを選択",
                option_type=7,
                required=False,
            ),
            create_option(
                name="channel",
                description="ミュートするチャンネル選択",
                option_type=7,
                required=False,
            ),
            create_option(
                name="role", description="ミュートするロールを選択", option_type=8, required=False
            ),
        ],
    )
    async def slash_say(
        self, ctx: SlashContext, target: int, category=None, channel=None, role=None
    ):
        target = MutingTargets(target)
        item = None
        if await self.bot.Check.com_per(ctx, target) is False:
            if ctx.guild is None:
                return await ctx.send("サーバーに関する設定はDMで実行できません。")
            if not ctx.author.guild_permissions.manage_guild:
                return await ctx.send("サーバーに関する設定は管理権限を持っているユーザーのみ実行できます。")

        # guild
        if target is MutingTargets.GUILD:
            mute_guilds = self.mute_configs.get("guilds")
            if ctx.guild.id not in mute_guilds:
                mute_guilds.append(ctx.guild.id)
                msg = "サーバーの展開をOFFにしました"
            else:
                mute_guilds.remove(ctx.guild.id)
                msg = "サーバーの展開をONにしました"

        # category
        elif target is MutingTargets.CATEGORY:
            item = category or ctx.channel.category
            if item is None:
                return await ctx.send("このコマンドをカテゴリー外チャンネルで実行する際は`category`オプションが必要です。")
            mute_list = self.mute_configs.get("categories")

        # channel
        elif target is MutingTargets.CHANNEL:
            item = channel or ctx.channel
            mute_list = self.mute_configs.get("channels")

        # role
        elif target is MutingTargets.ROLE:
            item = role
            if item is None:
                return await ctx.send("ロールが指定されていません。")
            mute_list = self.mute_configs.get("roles")

        # user
        elif target is MutingTargets.USER:
            item = ctx.author
            mute_list = self.mute_configs.get("users")

        if item:
            if item.id not in mute_list:
                mute_list.append(item.id)
                msg = f"{item.mention}の展開をOFFにしました"
            else:
                mute_list.remove(item.id)
                msg = f"{item.mention}の展開をONにしました"

        embed = discord.Embed(
            title="設定完了", description=msg, color=discord.Colour.blue()
        )
        await ctx.send(embed=embed)
        await self.write()


def setup(bot):
    bot.add_cog(Mute(bot))
