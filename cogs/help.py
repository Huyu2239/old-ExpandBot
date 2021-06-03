import asyncio

import discord
from discord.ext import commands
from discord_slash import SlashContext, cog_ext
from discord_slash.utils.manage_commands import create_choice, create_option


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        asyncio.create_task(self.bot.slash.sync_all_commands())
        self.help_em = [
            (
                discord.Embed(
                    title="概要",
                    description="Discordのメッセージリンクを展開するBotです。\n`/help <commands>`でコマンドの詳細を表示します。",
                    color=discord.Colour.blue()
                )
            ),
            (
                discord.Embed(
                    title="ping",
                    description="Botのレイテンシを返します。\n実行した人のレイテンシを返すものではありません。",
                    color=discord.Colour.blue()
                )
            )
        ]
        self.help_em[0].add_field(
            name='URL一覧',
            value="[サポートサーバー](https://discord.gg/CF49JQUnXV)\n[導入リンク](https://discord.com/api/oauth2/authorize?client_id=827863670507438130&permissions=85056&scope=bot%20applications.commands)"
        )
        self.help_em[0].add_field(
            name='動作サーバー数',
            value=f'{len(self.bot.guilds)}guilds'
        )
        self.help_em[0].add_field(
            name='総ユーザー数',
            value=f'{len(set(self.bot.get_all_members()))}users'
        )
        self.help_em[0].add_field(
            name='動作環境',
            value='[Tera-server](https://tera-server.com/)'
        )

    def cog_unload(self):
        self.bot.slash.remove_cog_commands(self)

    async def update_help_em(self):
        self.help_em[0].remove_field(1)
        self.help_em[0].remove_field(2)
        self.help_em[0].set_field_at(
            index=1,
            name='動作サーバー数',
            value=f'{len(self.bot.guilds)}guilds'
        )
        self.help_em[0].set_field_at(
            index=2,
            name='総ユーザー数',
            value=f'{len(set(self.bot.get_all_members()))}users'
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
    async def on_member_leave(self, guild):
        await self.update_help_em()

    async def compose_mute_em(self, ctx):
        mute_em = discord.Embed(
            title="mute",
            description="展開の無効化・有効化をします。",
            color=discord.Colour.blue()
        )
        # user_mute
        if ctx.author.id in self.bot.mute_data.get('users'):
            user_mute = True
        else:
            user_mute = False
        if ctx.guild is None:
            mute_em.add_field(
                name='`現在の設定`',
                value=f'```\nuser_mute={user_mute}\n```\n'
            )
            return mute_em
        # guild_mute
        if ctx.guild.id in self.bot.mute_data.get('guilds'):
            server_mute = True
        else:
            server_mute = False
        # category_mute
        if ctx.channel.category:
            if ctx.channel.category_id in self.bot.mute_data.get('categories'):
                category_mute = True
            else:
                category_mute = False
        else:
            category_mute = 'NotFound'
        # channel_mute
        if ctx.channel.id in self.bot.mute_data.get('channels'):
            channel_mute = True
        else:
            channel_mute = False
        # role_mute
        role_num = 1
        for role in ctx.author.roles:
            if role.id in self.bot.mute_data.get('roles'):
                role_num *= -1
        if role_num == -1:
            role_mute = True
        else:
            role_mute = False
        mute_em.add_field(
            name='`現在の設定`',
            value=f'```\nserver_mute={server_mute}\n```\n'
                  f'```\ncategory_mute={category_mute}\n```\n'
                  f'```\nchannel_mute={channel_mute}\n```\n'
                  f'```\nrole_mute={role_mute}\n```\n'
                  f'```\nuser_mute={user_mute}\n```\n'
        )
        return mute_em

    async def compose_set_em(self, ctx):
        set_em = discord.Embed(
            title="set",
            description="\n```\n展開に関する設定を行います。\n```\n",
            color=discord.Colour.blue()
        )
        if ctx.guild is None:
            data = self.bot.users_data.get(str(ctx.author.id))
            set_em.add_field(
                name='現在のユーザー設定',
                value='\n```\n変更はDMでのみ可能です。\n```\n',
                inline=False
            )
        else:
            guild_data = self.bot.guilds_data.get(str(ctx.guild.id))
            set_em.add_field(
                name='現在のメンバー設定',
                value='\n```\n変更はサーバーでのみ可能です。\n```\n',
                inline=False
            )
            if guild_data is None:
                guild_data = {}
            data = guild_data.get(str(ctx.author.id))
        if data is None:
            data = {}
        await self.add_set_fields(set_em, data)
        if ctx.guild:
            if ctx.author.guild_permissions.manage_guild:
                set_em.add_field(
                    name='現在のサーバー設定',
                    value='\n```\n変更はサーバー管理者のみ可能です。\n```\n',
                    inline=False
                )
                guild_data = self.bot.guilds_data.get(str(ctx.guild.id))
                await self.add_set_fields(set_em, guild_data)
        return set_em

    async def add_set_fields(self, set_em, data):
        set_em.add_field(
            name='[`hidden`](https://github.com/Huyu2239/ExpandBot/blob/add_docs/docs/set.md#hidden)',
            value=f'```\nhidden={data.get("hidden")}\n```\n'
        )
        set_em.add_field(
            name='[`anonymity`](https://github.com/Huyu2239/ExpandBot/blob/add_docs/docs/set.md#anonymity)',
            value=f'```\nanonymity={data.get("anonymous")}\n```\n'
        )
        set_em.add_field(
            name='[`embed_type`](https://github.com/Huyu2239/ExpandBot/blob/add_docs/docs/set.md#embed_type--embed_color)',
            value=f'```\nembed_type={data.get("embed_type")}\n```\n'
        )
        set_em.add_field(
            name='[`embed_color`](https://github.com/Huyu2239/ExpandBot/blob/add_docs/docs/set.md#embed_type--embed_color)',
            value=f'```\nembed_type=#{data.get("embed_color")}\n```\n'
        )
        set_em.add_field(
            name='[`allow`](https://github.com/Huyu2239/ExpandBot/blob/add_docs/docs/set.md#allow)',
            value=f'```\nallow={data.get("allow")}\n```\n'
        )

    @cog_ext.cog_slash(
        name='help',
        description='このBotのHelpを返します。',
        options=[
            create_option(
                name="command",
                description="helpを表示するコマンドを選択してください。",
                option_type=4, required=False,
                choices=[
                    create_choice(name="ping", value=1),
                    create_choice(name="set", value=2),
                    create_choice(name="mute", value=3)
                ]
            )
        ]
    )
    async def slash_say(self, ctx: SlashContext, command=None):
        if command is None:
            await ctx.send(embed=self.help_em[0])
        elif command == 1:
            await ctx.send(embed=self.help_em[1])
        elif command == 2:
            set_em = await self.compose_set_em(ctx)
            await ctx.send(embed=set_em)
        elif command == 3:
            mute_em = await self.compose_mute_em(ctx)
            await ctx.send(embed=mute_em)


def setup(bot):
    bot.add_cog(Help(bot))
