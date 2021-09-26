import asyncio
import traceback

import discord
from discord.ext import commands

EMOJI_ERROR_UNQUOTABLE = "\U0000274c"


class CommandErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.timeout = discord.Embed(
            title="ERROR", description="タイムアウトしました。", color=discord.Color.red()
        )

    async def error_log(self, str):
        try:
            await self.bot.get_channel(self.bot.log_ch_id).send(str)
        except discord.errors.HTTPException:
            await self.bot.get_channel(self.bot.log_ch_id).send("エラー文が文字数を超過しました")
            print(str)  # stderr

    @commands.Cog.listener()
    async def on_error(self, ctx, error):
        orig_error = getattr(error, "original", error)
        error_str = "".join(
            traceback.TracebackException.from_exception(orig_error).format()
        )
        await ctx.add_reaction(EMOJI_ERROR_UNQUOTABLE)
        await self.error_log(error_str)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        orig_error = getattr(error, "original", error)
        error_str = "".join(
            traceback.TracebackException.from_exception(orig_error).format()
        )
        print(error_str)  # stderr
        embed = discord.Embed(title="ERROR", color=discord.Colour.red())

        if hasattr(ctx.command, "on_error"):
            print("error")
            return
        # discord.ext error
        if isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.DisabledCommand):
            embed.add_field(
                name="DisabledCommand", value=f"無効化されたコマンドです。\n```py\n{error_str}```"
            )
        elif isinstance(error, commands.CheckFailure):
            embed.add_field(
                name="CheckFailure",
                value=f"このコマンドを実行する管理権限を保持していません。\n二度と実行しないでください。\n```py\n{error_str}```",
            )
        elif isinstance(error, commands.NoPrivateMessage):
            embed.add_field(
                name="NoPrivateMessage",
                value=f"DMでこのコマンドは実行できません。\n```py\n{error_str}```",
            )
        elif isinstance(error, commands.BadArgument):
            embed.add_field(
                name="BadArgument", value=f"因数が無効です。\n```py\n{error_str}```"
            )
        elif isinstance(error, commands.MissingPermissions):
            embed.add_field(
                name="MissingPermissions",
                value=f"{','.join(error.missing_perms)}の権限がありません。\n```py\n{error_str}```",
            )
        elif isinstance(error, commands.BotMissingPermissions):
            embed.add_field(
                name="BotMissingPermissions",
                value=f"Botに{','.join(error.missing_perms)}の権限が付与されていません。\n権限を確認してください。\n```py\n{error_str}```",
            )
        else:
            embed.add_field(
                name="UnknownError",
                value=f"予期しないエラーが発生しました。\n必ず報告してください。\n```py\n{error_str}```",
            )
        await ctx.message.add_reaction(EMOJI_ERROR_UNQUOTABLE)
        try:
            await ctx.send("エラーが発生しました\nスクショなどの情報と一緒にサポートサーバーまで連絡してください", embed=embed)
        except discord.errors.HTTPException:
            await ctx.send("エラーが発生しました\nスクショなどの情報と一緒にサポートサーバーまで連絡してください")

        error_msg = f"```py\n{error_str}\n```\ncommand={ctx.message.content}"
        await self.error_log(error_msg)

    @commands.Cog.listener()
    async def on_slash_command_error(self, ctx, error):
        orig_error = getattr(error, "original", error)
        error_str = "".join(
            traceback.TracebackException.from_exception(orig_error).format()
        )

        if isinstance(error, asyncio.TimeoutError):
            return await ctx.send(embed=self.timeout)

        embed = discord.Embed(title="ERROR", colour=discord.Colour.red())
        embed.add_field(name="内部エラー\nサポートサーバーまでご連絡ください", value=f"```py\n{error_str}```")
        await ctx.add_reaction(EMOJI_ERROR_UNQUOTABLE)
        try:
            await ctx.send(embed=embed)
        except discord.errors.HTTPException:
            await ctx.send("エラー発生")
        await self.error_log(f"```py\n{error_str}```")


def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))
