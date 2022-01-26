import asyncio

import discord
from discord.ext import commands
from discord_slash import SlashContext, cog_ext
from discord_slash.utils.manage_commands import create_choice, create_option
from libs import HelpTargetCommands, MutingTarget, MuteConfigs


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        asyncio.create_task(self.bot.slash.sync_all_commands())
        self.help_em = discord.Embed(
            title="概要",
            description="Discordのメッセージリンクを展開するBotです。\n`/ヘルプ <コマンド>`でコマンドの詳細を表示します。",
            color=discord.Colour.blue(),
        )
        self.help_em.add_field(
            name="URL一覧",
            value="[サポートサーバー](https://discord.gg/CF49JQUnXV)\n[導入リンク](https://discord.com/api/oauth2/authorize?client_id=827863670507438130&permissions=85056&scope=bot%20applications.commands)",
        )
        self.help_em.add_field(name="動作サーバー数", value=f"{len(self.bot.guilds)}サーバー")
        self.help_em.add_field(
            name="総ユーザー数", value=f"{len(set(self.bot.get_all_members()))}ユーザー"
        )
        self.wiki_url = "https://github.com/Huyu2239/ExpandBot/wiki"

    def cog_unload(self):
        self.bot.slash.remove_cog_commands(self)

    async def update_help_em(self):
        self.help_em.set_field_at(
            index=1, name="動作サーバー数", value=f"{len(self.bot.guilds)}サーバー"
        )
        self.help_em.set_field_at(
            index=2, name="総ユーザー数", value=f"{len(set(self.bot.get_all_members()))}ユーザー"
        )

    @commands.Cog.listener()
    async def on_guild_join(self, _):
        await self.update_help_em()

    @commands.Cog.listener()
    async def on_guild_remove(self, _):
        await self.update_help_em()

    @commands.Cog.listener()
    async def on_member_join(self, _):
        await self.update_help_em()

    @commands.Cog.listener()
    async def on_member_leave(self, _):
        await self.update_help_em()

    async def compose_mute_embed(self, ctx):
        mute_embed = discord.Embed(
            title="ミュート",
            description="展開のミュートをします。\n" f"[公式ドキュメント]({self.wiki_url}/ミュート)",
            color=discord.Colour.blue(),
        )
        # ユーザー
        user_mute = await MuteConfigs.read(ctx.author.id, MutingTarget.USER)
        mute_display = f"ユーザー: {utils.convert_to_emoji_from_bool(user_mute)}"
        if ctx.guild is None:
            mute_embed.add_field(name="`現在の設定`", value=mute_display)
            return mute_embed
        # サーバー
        guild_mute = await MuteConfigs.read(ctx.guild.id, MutingTarget.GUILD)
        mute_display += f"\nサーバー: {utils.convert_to_emoji_from_bool(guild_mute)}"
        # カテゴリー
        if ctx.channel.category:
            category_mute = await MuteConfigs.read(ctx.channel.category_id, MutingTarget.CATEGORY)
            mute_display += f"\nカテゴリー: {utils.convert_to_emoji_from_bool(category_mute)}"
        # チャンネル
        channel_mute = await MuteConfigs.read(ctx.channel.id, MutingTarget.CHANNEL)
        mute_display += f"\nチャンネル: {utils.convert_to_emoji_from_bool(channel_mute)}"
        # ロール
        role_num = 1
        for role in ctx.author.roles:
            if await MuteConfigs.read(role.id, MutingTarget.ROLE):
                role_num *= -1
        mute_display += f"\nロール: {utils.convert_to_emoji_from_bool(role_num == -1)}"
        mute_embed.add_field(
            name="`現在の設定`",
            value=mute_display,
        )
        return mute_embed

    async def compose_set_embed(self, ctx):
        set_embed = discord.Embed(
            title="set",
            description=f"[公式ドキュメント]({self.wiki_url}/設定)\n"
            "\n```\n展開に関する設定を行います。\n```\n\n",
            color=discord.Colour.blue(),
        )
        if ctx.guild is None:
            user_config = self.bot.users_data.get(str(ctx.author.id))
            set_embed.add_field(
                name="現在のユーザー設定", value="\n```\n変更はDMでのみ可能です。\n```\n", inline=False
            )
        else:
            guild_data = self.bot.guilds_data.get(str(ctx.guild.id))
            set_embed.add_field(
                name="現在のメンバー設定", value="\n```\n変更はサーバーでのみ可能です。\n```\n", inline=False
            )
            if guild_data is None:
                guild_data = {}
            data = guild_data.get(str(ctx.author.id))
        if data is None:
            data = {}
        await ctx.send(embed=await self.add_set_fields(set_em, data))
        if ctx.guild:
            set_emb = discord.Embed()
            set_emb.add_field(
                name=" \n \n現在のサーバー設定",
                value="\n```\n変更はサーバー管理者のみ可能です。\n```\n",
                inline=False,
            )
            guild_data = self.bot.guilds_data.get(str(ctx.guild.id))
            if guild_data is None:
                guild_data = {}
            await ctx.send(embed=await self.add_set_fields(set_emb, guild_data))

    async def add_set_fields(self, set_em, data):
        vals = ["hidden", "anonymity"]
        for val in vals:
            if data.get(val) is True:
                val_bool = "<:True:850591234283798558>"
            elif data.get(val) is False:
                val_bool = "<:False:850591522171912202>"
            else:
                val_bool = "<:None:850591553688436746>"
            set_em.add_field(
                name="\u200b",
                value=f"[`{val}`]({self.wiki_url}): {val_bool}",
            )
        set_em.add_field(name="\u200b", value="\u200b")
        set_em.add_field(
            name="\u200b",
            value=f"[`embed_type`]({self.wiki_url})"
            f'```\n{data.get("embed_type")}\n```\n',
        )
        set_em.add_field(
            name="\u200b",
            value=f"[`embed_color`]({self.wiki_url})"
            f'```\n#{data.get("embed_color")}\n```\n',
        )
        set_em.add_field(
            name="\u200b",
            value=f"[`allow`]({self.wiki_url})" f'```\n{data.get("allow")}\n```\n',
        )
        return set_em

    @cog_ext.cog_slash(
        name="ヘルプ",
        description="このBotのヘルプを返します。",
        options=[
            create_option(
                name="コマンド",
                description="ヘルプを表示するコマンドを選択してください。",
                option_type=4,
                required=False,
                choices=[
                    create_choice(name="ミュート", value=HelpTargetCommands.MUTE),
                    create_choice(name="設定", value=HelpTargetCommands.SET),
                ],
            )
        ],
    )
    async def slash_say(self, ctx: SlashContext, command=None):
        # none
        if command is None:
            return await ctx.send(embed=self.help_em)
        command = HelpTargetCommands(command)
        # mute
        if command is HelpTargetCommands.MUTE:
            mute_embed = await self.compose_mute_embed(ctx)
            return await ctx.send(embed=mute_em)
        # set
        elif command is HelpTargetCommands.SET:
            set_embed = await self.compose_set_embed(ctx)
            return await ctx.send(embed=set_embed)


def setup(bot):
    bot.add_cog(Info(bot))
