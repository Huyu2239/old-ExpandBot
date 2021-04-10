import discord
from discord.ext import commands  # , tasks
from discord_slash import SlashContext, cog_ext  # SlashCommand
# from discord_slash.utils import manage_commands

import asyncio


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        asyncio.create_task(self.bot.slash.sync_all_commands())
        self.help_em = self.compose_help()

    def cog_unload(self):
        self.bot.slash.remove_cog_commands(self)

    def compose_help(self):
        help_em = [
            (
                discord.Embed(
                    title="概要",
                    description="Discordのメッセージリンクを展開するBotです。",
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
            value='このメッセージを送信します'
        )
        help_em[1].add_field(
            name='`/embed_type`（未実装）',
            value='展開メッセージの装飾を変更できます\nデフォルトは1です'
        )
        help_em[1].add_field(
            name='`/public`',
            value='サーバー内のメッセージのリンクが他のサーバーに送信された場合の展開の**ON・OFF**を切り替えます\n送信元の設定がOFFの場合はリンク先のサーバーの設定がONの場合でも展開**されません**',
            inline=False
        )
        return help_em

    @cog_ext.cog_slash(name='help', description='このBotのHelpを返します。', guild_ids=[829431106263580703])
    async def slash_say(self, ctx: SlashContext):
        # await ctx.respond(eat=True)
        page = 0
        help_msg = await ctx.send(embed=self.help_em[page])
        emoji = '➡'
        await help_msg.add_reaction(emoji)
        while True:
            def reaction_check(reaction, user):
                if reaction.message.id == help_msg.id \
                        and user == ctx.author:
                    return reaction, user

            try:
                reaction, user = await self.bot.wait_for(
                    "reaction_add", timeout=60.0, check=reaction_check)
                emoji = str(reaction.emoji)
            except asyncio.TimeoutError:
                await help_msg.remove_reaction(emoji, self.bot.user)
                return
            # await help_msg.remove_reaction(emoji, user)
            if page == len(self.help_em) - 1:
                # 最大の時は最初に
                page = 0
            else:
                # その他は一つ上がる
                page += 1
            await help_msg.edit(embed=self.help_em[page])


def setup(bot):
    bot.add_cog(Help(bot))
