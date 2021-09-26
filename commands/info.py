import asyncio

import discord
from discord.ext import commands
from discord_slash import SlashContext, cog_ext
from discord_slash.utils.manage_commands import create_choice, create_option
from libs import HelpTargetCommands


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        asyncio.create_task(self.bot.slash.sync_all_commands())
        self.help_em = [
            (
                discord.Embed(
                    title="概要",
                    description="Discordのメッセージリンクを展開するBotです。\n`/ヘルプ <コマンド>`でコマンドの詳細を表示します。",
                    color=discord.Colour.blue(),
                )
            ),
            (
                discord.Embed(
                    title="ping",
                    description="Botのレイテンシを返します。\n実行した人のレイテンシを返すものではありません。",
                    color=discord.Colour.blue(),
                )
            ),
        ]
        self.help_em[0].add_field(
            name="URL一覧",
            value="[サポートサーバー](https://discord.gg/CF49JQUnXV)\n[導入リンク](https://discord.com/api/oauth2/authorize?client_id=827863670507438130&permissions=85056&scope=bot%20applications.commands)",
        )
        self.help_em[0].add_field(name="動作サーバー数", value=f"{len(self.bot.guilds)}サーバー")
        self.help_em[0].add_field(
            name="総ユーザー数", value=f"{len(set(self.bot.get_all_members()))}ユーザー"
        )
        self.wiki_url = "https://github.com/Huyu2239/ExpandBot/wiki"

    def cog_unload(self):
        self.bot.slash.remove_cog_commands(self)

    async def update_help_em(self):
        self.help_em[0].set_field_at(
            index=1, name="動作サーバー数", value=f"{len(self.bot.guilds)}サーバー"
        )
        self.help_em[0].set_field_at(
            index=2, name="総ユーザー数", value=f"{len(set(self.bot.get_all_members()))}ユーザー"
        )

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        await self.update_help_em()

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        await self.update_help_em()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await self.update_help_em()

    @commands.Cog.listener()
    async def on_member_leave(self, member):
        await self.update_help_em()

    async def compose_mute_em(self, ctx):
        self.mute_configs = self.bot.get_cog("Mute").mute_configs
        mute_em = discord.Embed(
            title="ミュート",
            description="展開のミュートをします。\n" f"[公式ドキュメント]({self.wiki_url}/ミュート)",
            color=discord.Colour.blue(),
        )
        user_mute = ctx.author.id in self.bot.mute_configs.get("users")
        if ctx.guild is None:
            mute_em.add_field(name="`現在の設定`", value=f"```\nユーザー={user_mute}\n```\n")
            return mute_em
        server_mute = ctx.guild.id in self.bot.mute_configs.get("guilds")
        category_mute = ctx.channel.category_id in self.bot.mute_configs.get(
            "categories"
        )
        if ctx.channel.category is None:
            category_mute = "NotFound"
        channel_mute = ctx.channel.id in self.bot.mute_configs.get("channels")
        # role_mute
        role_num = 1
        for role in ctx.author.roles:
            if role.id in self.mute_configs.get("roles"):
                role_num *= -1
        role_mute = role_num == -1
        mute_em.add_field(
            name="`現在の設定`",
            value=f"```\nサーバー={server_mute}\n```\n"
            f"```\nカテゴリー={category_mute}\n```\n"
            f"```\nチャンネル={channel_mute}\n```\n"
            f"```\nロール={role_mute}\n```\n"
            f"```\nユーザー={user_mute}\n```\n",
        )
        return mute_em

    async def send_set_em(self, ctx):
        set_em = discord.Embed(
            title="set",
            description=f"[公式ドキュメント]({self.wiki_url}/設定)\n"
            "\n```\n展開に関する設定を行います。\n```\n\n",
            color=discord.Colour.blue(),
        )
        if ctx.guild is None:
            data = self.bot.users_data.get(str(ctx.author.id))
            set_em.add_field(
                name="現在のユーザー設定", value="\n```\n変更はDMでのみ可能です。\n```\n", inline=False
            )
        else:
            guild_data = self.bot.guilds_data.get(str(ctx.guild.id))
            set_em.add_field(
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
                name="command",
                description="helpを閲覧するコマンドを選択してください。",
                option_type=4,
                required=False,
                choices=[
                    create_choice(name="ping", value=HelpTargetCommands.PING),
                    create_choice(name="mute", value=HelpTargetCommands.MUTE),
                    create_choice(name="set", value=HelpTargetCommands.SET),
                ],
            )
        ],
    )
    async def slash_say(self, ctx: SlashContext, command=None):
        # none
        if command is None:
            return await ctx.send(embed=self.help_em[0])
        command = HelpTargetCommands(command)
        # ping
        if command is HelpTargetCommands.PING:
            return await ctx.send(embed=self.help_em[1])
        # mute
        elif command is HelpTargetCommands.MUTE:
            mute_em = await self.compose_mute_em(ctx)
            return await ctx.send(embed=mute_em)
        # set
        elif command is HelpTargetCommands.SET:
            return await self.send_set_em(ctx)


def setup(bot):
    bot.add_cog(Info(bot))
