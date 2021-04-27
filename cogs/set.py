import asyncio
import libs.database
import discord
from discord.ext import commands
from discord_slash import SlashContext, cog_ext
from discord_slash.utils.manage_commands import create_choice, create_option


class Set(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        asyncio.create_task(self.bot.slash.sync_all_commands())

    def cog_unload(self):
        self.bot.slash.remove_cog_commands(self)

    async def compose_setting_em(self, target_dict, target_name):
        embed = discord.Embed(description='設定完了')
        embed.add_field(
            name=target_name,
            value=f'```\nhidden={target_dict.get("hidden")}\n```\n'
                  f'```\nanonymous={target_dict.get("anonymous")}\n```\n'
                  f'```\nembed_type={target_dict.get("embed_type")}\n```\n'
                  f'```\nembed_color={target_dict.get("embed_color")}\n```\n'
        )

    @cog_ext.cog_slash(
        name='set',
        description='展開に関する設定を行います。',
        options=[
            create_option(
                name="target",
                description="設定する対象を選択してください。",
                option_type=4, required=True,
                choices=[
                    create_choice(name="server", value=1),
                    create_choice(name="channel", value=2),
                    create_choice(name="user", value=3)
                ]
            ),
            create_option(
                name="topic",
                description="設定する項目を選択してください。",
                option_type=4, required=True,
                choices=[
                    create_choice(name="hidden", value=1),
                    create_choice(name="anonymous", value=2),
                    create_choice(name="embed_type", value=3),
                    create_choice(name="embed_color", value=4)
                ]
            ),
            create_option(
                name="channel",
                description="別チャンネルの設定をする場合は、そのチャンネルを指定してください。(未入力の場合は送信したチャンネル)",
                option_type=7, required=False
            ),
            create_option(
                name="embed_type",
                description="展開のembedのタイプを選択してください。",
                option_type=4, required=False,
                choices=[
                    create_choice(name="1", value=1)
                ]
            ),
            create_option(
                name="embed_color",
                description="embedに使用するカラーを16進数で指定してください。無効なカラーを指定した場合展開されません",
                option_type=7, required=False
            )
        ]
    )
    async def slash_say(self, ctx: SlashContext, target, topic, embed_type=None, embed_color=None, channel=None):
        # 設定するdictを汎用化
        if target == 1:
            target_dict = self.bot.guilds_data.get(str(ctx.guild.id))
            target_name = f'on {ctx.guild.name}'
        '''
        if target == 2:
            if channel:
                target_dict = self.bot.channels_data.get(str(channel.id))
                target_name = f'on <#{channel.id}>'
            else:
                target_dict = self.bot.channels_data.get(str(ctx.channel.id))
                target_name = f'on <#{ctx.channel.id}>'
        if target == 3:
            pass
            target_dict = self.bot.users_data.get(str(ctx.author.id))
            target_name = f'on <@{ctx.author.id}>'
        '''
        if target_dict is None:
            if target == 1:
                target_dict = await libs.database.Database.write_new_data(self.bot.guilds_data, ctx.guild.id)  # guilds_data
            else:
                return
            '''
            if target == 2:
                await libs.database.Database.write_new_data(self.bot.guilds_data)  # channels_data
            if target == 3:
                await libs.database.Database.write_new_data(self.bot.guilds_data)  # users_data
            '''
            # databaseでtmpを書き込み

        # dictの上書き
        if topic == 1:
            if target_dict.get('hidden') is False:
                target_dict['hidden'] = True
            else:
                target_dict['hidden'] = False
        if topic == 2:
            if target_dict.get('anonymous') is False:
                target_dict['anonymous'] = True
            else:
                target_dict['anonymous'] = False
        if topic == 3:
            if embed_type is None:
                embed = discord.Embed(title='ERROR', description='embed_typeが指定されていません。', color=discord.Colour.red())
                return await ctx.send(embed=embed)
            target_dict['embed_type'] = embed_type
        if topic == 4:
            if embed_color is None:
                embed = discord.Embed(title='ERROR', description='embed_colorが指定されていません。', color=discord.Colour.red())
                return await ctx.send(embed=embed)
            target_dict['embed_color'] = embed_color

        # レスポンス
        embed = await self.compose_setting_em(target_dict, target_name)
        await ctx.send(embed=embed)
        await libs.database.Database.write_all_data(self.bot)


def setup(bot):
    bot.add_cog(Set(bot))
