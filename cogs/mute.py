import asyncio

import discord

from discord.ext import commands
from discord_slash import SlashContext, cog_ext
from discord_slash.utils.manage_commands import create_choice, create_option


class Mute(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        asyncio.create_task(self.bot.slash.sync_all_commands())

    def cog_unload(self):
        self.bot.slash.remove_cog_commands(self)

    async def set_guild_mute(self, ctx):
        mute_guilds = self.bot.mute_data.get('guilds')
        if ctx.guild.id in mute_guilds:
            mute_guilds.remove(ctx.guild.id)
            return 'サーバーの展開をONにしました'
        else:
            mute_guilds.append(ctx.guild.id)
            return 'サーバーの展開をOFFにしました'

    async def set_category_mute(self, value, ctx):
        item = int()
        if value is None:
            if ctx.channel.category:
                item = ctx.channel.category_id
            else:
                return await ctx.send('このコマンドをカテゴリー外チャンネルで実行する際は`category`オプションが必要です。')
        else:
            item = value.id
        mute_categories = self.bot.mute_data.get('categories')
        if item in mute_categories:
            mute_categories.remove(item)
            return f'<#{item}>の展開をONにしました'
        else:
            mute_categories.append(item)
            return f'<#{item}>の展開をOFFにしました'

    async def set_channel_mute(self, value, ctx):
        item = int()
        if value is None:
            item = ctx.channel.id
        else:
            item = value.id
        mute_channels = self.bot.mute_data.get('channels')
        if item in mute_channels:
            mute_channels.remove(item)
            return f'<#{item}>の展開をONにしました'
        else:
            mute_channels.append(item)
            return f'<#{item}>の展開をOFFにしました'

    async def set_role_mute(self, value, ctx):
        if value is None:
            return await ctx.send('ロールが指定されていません。')
        item = value.id
        mute_roles = self.bot.mute_data.get('roles')
        if item in mute_roles:
            mute_roles.remove(item)
            return f'<@&{item}>の展開をONにしました'
        else:
            mute_roles.append(item)
            return f'<@&{item}>の展開をOFFにしました'

    async def set_user_mute(self, ctx):
        mute_users = self.bot.mute_data.get('users')
        if ctx.author.id in mute_users:
            mute_users.remove(ctx.author.id)
            return f'<@{ctx.author.id}>の展開をONにしました'
        else:
            mute_users.append(ctx.author.id)
            return f'<@{ctx.author.id}>の展開をOFFにしました'

    @cog_ext.cog_slash(
        name='mute',
        description='展開の無効化・有効化をします。',
        options=[
            create_option(
                name="target",
                description="muteする対象を選択",
                option_type=4, required=True,
                choices=[
                    create_choice(name="server", value=1),
                    create_choice(name="category", value=2),
                    create_choice(name="channel", value=3),
                    create_choice(name="role", value=4),
                    create_choice(name="user", value=5)
                ]
            ),
            create_option(
                name="category",
                description="muteするカテゴリーを選択",
                option_type=7, required=False
            ),
            create_option(
                name="channel",
                description="muteするチャンネル選択",
                option_type=7, required=False
            ),
            create_option(
                name="role",
                description="muteするロールを選択",
                option_type=8, required=False
            )
        ]
    )
    async def slash_say(self, ctx: SlashContext, target, category=None, channel=None, role=None):
        if await self.bot.check.check_com_per(ctx, target) is False:
            return
        msg = str()
        if target == 1:
            msg = await self.set_guild_mute(ctx)
        if target == 2:
            msg = await self.set_channel_mute(category, ctx)
        if target == 3:
            msg = await self.set_channel_mute(channel, ctx)
        if target == 4:
            msg = await self.set_role_mute(role, ctx)
        if target == 5:
            msg = await self.set_user_mute(ctx)
        if msg is None:
            return
        embed = discord.Embed(title='設定完了', description=msg, color=discord.Colour.blue())
        await ctx.send(embed=embed)
        await self.bot.database.Mute_Data.write(self.bot)


def setup(bot):
    bot.add_cog(Mute(bot))
