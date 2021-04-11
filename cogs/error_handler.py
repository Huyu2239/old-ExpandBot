import traceback
from discord.ext import commands
import discord


class CommandErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        orig_error = getattr(error, "original", error)
        error_str = ''.join(traceback.TracebackException.from_exception(orig_error).format())
        print(error_str)  # stderr
        embed = discord.Embed(title='ERROR', color=discord.Colour.red())

        if hasattr(ctx.command, 'on_error'):
            print('error')
            return
        # discord.ext error
        if isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.DisabledCommand):
            embed.add_field(
                name='DisabledCommand',
                value=f'無効化されたコマンドです。\n```py\n{error_str}```'
            )
        elif isinstance(error, commands.CheckFailure):
            embed.add_field(
                name='CheckFailure',
                value=f'このコマンドを実行する管理権限を保持していません。\n二度と実行しないでください。\n```py\n{error_str}```'
            )
        elif isinstance(error, commands.NoPrivateMessage):
            embed.add_field(
                name='NoPrivateMessage',
                value=f'DMでこのコマンドは実行できません。\n```py\n{error_str}```'
            )
        elif isinstance(error, commands.BadArgument):
            embed.add_field(
                name='BadArgument',
                value=f'因数が無効です。\n```py\n{error_str}```'
            )
        elif isinstance(error, commands.MissingPermissions):
            embed.add_field(
                name='MissingPermissions',
                value=f"{','.join(error.missing_perms)}の権限がありません。\n```py\n{error_str}```"
            )
        elif isinstance(error, commands.BotMissingPermissions):
            embed.add_field(
                name='BotMissingPermissions',
                value=f"Botに{','.join(error.missing_perms)}の権限が付与されていません。\n権限を確認してください。\n```py\n{error_str}```"
            )
        else:
            embed.add_field(
                name='UnknownError',
                value=f"予期しないエラーが発生しました。\n必ず報告してください。\n```py\n{error_str}```"
            )
        try:
            await ctx.send('エラーが発生しました\nスクショなどの情報と一緒にサポートサーバーまで連絡してください', embed=embed)
        except discord.errors.HTTPException:
            await ctx.send('エラーが発生しました\nスクショなどの情報と一緒にサポートサーバーまで連絡してください')
        error_msg = f"```py\n{error_str}\n```\ncommand={ctx.message.content}"
        try:
            await self.bot.get_channel(self.bot.log_ch_id).send(error_msg)
        except discord.errors.HTTPException:
            await self.bot.get_channel(self.bot.log_ch_id).send('文字数を超過しました')
        print(error_msg)


def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))
