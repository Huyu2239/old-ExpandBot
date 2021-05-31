import asyncio

import discord
from discord.ext import commands
from discord_slash import SlashContext, cog_ext
from discord_slash.utils.manage_commands import create_choice, create_option


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        asyncio.create_task(self.bot.slash.sync_all_commands())

    def cog_unload(self):
        self.bot.slash.remove_cog_commands(self)

    async def compose_help_em(self):
        help_em = [
            (
                discord.Embed(
                    title="概要",
                    description="Discordのメッセージリンクを展開するBotです。\n`/help <commands>`でコマンドの詳細を表示します。",
                    color=discord.Colour.blue()
                )
            ),
            (
                discord.Embed(
                    title="コマンド一覧",
                    color=discord.Colour.blue()
                )
            )
        ]
        help_em[0].add_field(
            name='URL一覧',
            value="[サポートサーバー](https://discord.gg/CF49JQUnXV)\n[導入リンク](https://discord.com/api/oauth2/authorize?client_id=827863670507438130&permissions=85056&scope=bot%20applications.commands)"
        )
        help_em[0].add_field(
            name='動作サーバー数',
            value=f'{len(self.bot.guilds)}guilds'
        )
        help_em[0].add_field(
            name='総ユーザー数',
            value=f'{len(set(self.bot.get_all_members()))}users'
        )
        help_em[0].add_field(
            name='動作環境',
            value='[Tera-server](https://tera-server.com/)'
        )
        help_em[1].add_field(
            name='`/help`',
            value='このメッセージを送信します。'
        )
        help_em[1].add_field(
            name='`/ping`',
            value='pongを返します。'
        )
        help_em[1].add_field(
            name='`/set`',
            value='展開に関する設定をします。'
        )
        help_em[1].add_field(
            name='`/mute`',
            value='展開の無効化・有効化をします。'
        )
        return help_em

    async def compose_com_em(self, ctx):
        com_em = [
            (
                discord.Embed(
                    title="ping",
                    description="Botのレイテンシを返します。\n実行した人のレイテンシを返すものではありません。",
                    color=discord.Colour.blue()
                )
            ),
            (
                discord.Embed(
                    title="mute",
                    description="展開の無効化・有効化をします。",
                    color=discord.Colour.blue()
                )
            )
        ]
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
        # user_mute
        if ctx.author.id in self.bot.mute_data.get('users'):
            user_mute = True
        else:
            user_mute = False
        com_em[1].add_field(
            name='`現在の設定`',
            value=f'```\nserver_mute={server_mute}\n```\n'
                  f'```\ncategory_mute={category_mute}\n```\n'
                  f'```\nchannel_mute={channel_mute}\n```\n'
                  f'```\nrole_mute={role_mute}\n```\n'
                  f'```\nuser_mute={user_mute}\n```\n'
        )
        return com_em

    async def compose_set_em(self, ctx):
        set_em = discord.Embed(
            title="set",
            description="展開に関する設定を行います。",
            color=discord.Colour.blue()
        )
        if ctx.guild:
            data = self.bot.guilds_data.get(str(ctx.guild.id))
        else:
            data = self.bot.users_data.get(str(ctx.author.id))
        if data is None:
            data = {}
        set_em.add_field(
            name='`hidden`',
            value='メッセージのリンクがサーバー外で送信された際に、\nメッセージを保護して展開しないように設定できます。\n'
                  f'```\nhidden={data.get("hidden")}\n```\n'
        )
        set_em.add_field(
            name='`anonymity`',
            value='メッセージのリンクがサーバー外で送信された際に、\nユーザー名を保護して表示しないように設定できます。\n'
                  f'```\nanonymity={data.get("anonymous")}\n```\n'
        )
        set_em.add_field(
            name='`embed_type`',
            value='メッセージのリンクが送信された際に、\nどのような形式で展開するのかを選択できます。\n'
                  f'```\nembed_type={data.get("embed_type")}\n```\n'
        )
        set_em.add_field(
            name='`embed_color`',
            value='メッセージのリンクが送信された際の埋め込みの色を指定できます。\n'
                  f'```\nembed_type={data.get("embed_color")}\n```\n'
        )
        set_em.add_field(
            name='`allow`',
            value='メッセージのリンクがサーバー外で送信された際かつhiddenがtrueの場合、\n特別に展開を許可するサーバー、ユーザー、チャンネルを指定できます。\nhiddenがfalseの場合は関係なく展開されます。\n'
                  f'```\nallow={data.get("allow")}\n```\n'
        )
        return set_em

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
            # await ctx.respond(eat=True)
            page = 0
            help_em = await self.compose_help_em()
            help_msg = await ctx.send(embed=help_em[page])
            emoji = '➡'
            await help_msg.add_reaction(emoji)
            while True:
                def reaction_check(reaction, user):
                    if reaction.message.id == help_msg.id \
                            and user == ctx.author:
                        return reaction, user

                try:
                    reaction, user = await self.bot.wait_for("reaction_add", timeout=60.0, check=reaction_check)
                    emoji = str(reaction.emoji)
                except asyncio.TimeoutError:
                    await help_msg.remove_reaction(emoji, self.bot.user)
                    return
                if page == len(help_em) - 1:
                    page = 0
                else:
                    page += 1
                await help_msg.edit(embed=help_em[page])
            return
        elif command == 1:
            com_em = await self.compose_com_em(ctx)
            await ctx.send(embed=com_em[0])
        elif command == 2:
            set_em = await self.compose_set_em(ctx)
            await ctx.send(embed=set_em)
        elif command == 3:
            com_em = await self.compose_com_em(ctx)
            await ctx.send(embed=com_em[1])


def setup(bot):
    bot.add_cog(Help(bot))
