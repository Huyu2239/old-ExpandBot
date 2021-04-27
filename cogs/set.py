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
                name="channel",
                description="別チャンネルの設定をする場合は、そのチャンネルを指定してください。(未入力の場合は送信したチャンネル)",
                option_type=7, required=False
            ),
            create_option(
                name="topic",
                description="設定する項目を選択してください。",
                option_type=4, required=True,
                choices=[
                    create_choice(name="hidden", value=1),
                    create_choice(name="anonimity", value=2),
                    create_choice(name="embed_type", value=3),
                    create_choice(name="embed_color", value=4)
                ]
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
    async def slash_say(self, ctx: SlashContext, target, topic, embed_type=None, embed_color=None, channel=None, ):
        # 設定するdictを汎用化
        if target == 1:
            target_dict = self.bot.guilds_data.get(str(ctx.guild.id))
        if target == 2:
            pass
            '''
            data = self.bot.channels_data
            if channel:
                target_id = channel.id
            else:
                target_id = ctx.channel.id
            '''
        if target == 3:
            pass
            # data=self.bot.users_data
            # target_id = ctx.author.id
        if target_dict is None:
            if target == 1:
                pass  # guilds_data
            if target == 2:
                pass  # channels_data
            if target == 3:
                pass  # users_data
            # databaseでtmpを書き込み

        # dictの上書き
        if topic == 1:
            if target_dict.get('hidden') is (False or None):
                target_dict['hidden'] = True
            else:
                target_dict['hidden'] = False
            msg = f'hidden={target_dict.get("hidden")}'
        if topic == 2:
            if target_dict.get('hidden') is (False or None):
                target_dict['hidden'] = True
            else:
                target_dict['hidden'] = False
            msg = f'hidden={target_dict.get("hidden")}'
        if topic == 3:
            if embed_type is None:
                msg = 'embedのtypeを指定してください。'
            target_dict['embed_type'] = embed_type
            msg = f'embed_type={embed_type}'
        if topic == 4:
            if embed_color is None:
                msg = 'embedのtypeを指定してください。'
            target_dict['embed_color'] = embed_color
            msg = f'embed_color={embed_color}'

        # レスポンス
        embed = discord.Embed(title='設定完了', description=msg, color=discord.Colour.blue())
        await ctx.send(embed=embed)
        await libs.database.Database.write_all_data(self.bot)


def setup(bot):
    bot.add_cog(Set(bot))
