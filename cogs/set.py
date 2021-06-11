import asyncio

import discord
from discord.ext import commands
from discord_slash import SlashContext, cog_ext
from discord_slash.utils.manage_commands import create_choice, create_option


class Set(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        asyncio.create_task(self.bot.slash.sync_all_commands())
        self.timeout = discord.Embed(title="ERROR", description="タイムアウトしました。")

    def cog_unload(self):
        self.bot.slash.remove_cog_commands(self)

    async def compose_set_em(self, target_dict, target_name):
        embed = discord.Embed(
            title=target_name,
            description="設定する項目を番号で選択してください。\n0: 終了",
            colour=int(f'0x{target_dict.get("embed_color")}', 16),
        )
        embed.add_field(
            name="1: hidden", value=f'```\n{target_dict.get("hidden")}\n```'
        )
        embed.add_field(
            name="2: anonymity", value=f'```\n{target_dict.get("anonymity")}\n```'
        )
        embed.add_field(
            name="3: embed_type", value=f'```\n{target_dict.get("embed_type")}\n```'
        )
        embed.add_field(
            name="4: embed_color", value=f'```\n#{target_dict.get("embed_color")}\n```'
        )
        embed.add_field(name="5: allow", value=f'```\n{target_dict.get("allow")}\n```')
        return embed

    @cog_ext.cog_slash(
        name="set",
        description="展開に関する設定",
        options=[
            create_option(
                name="target",
                description="設定する対象を選択",
                option_type=4,
                required=True,
                choices=[
                    create_choice(name="server", value=1),
                    create_choice(name="user", value=0),
                ],
            )
        ],
    )
    async def slash_say(self, ctx: SlashContext, target):
        if await self.bot.Check.com_per(ctx, target) is False:
            return
        if target == 1:
            target_dict = self.bot.guilds_data.get(str(ctx.guild.id))
            if target_dict is None:
                await self.bot.database.write_new_data(
                    self.bot.guilds_data, ctx.guild.id
                )
                target_dict = self.bot.guilds_data.get(str(ctx.guild.id))
            target_name = f"Server: {ctx.guild.name}"
        if target == 0:
            if ctx.guild is None:
                target_dict = self.bot.users_data.get(str(ctx.author.id))
                if target_dict is None:
                    await self.bot.database.write_new_data(
                        self.bot.users_data, ctx.author.id
                    )
                    target_dict = self.bot.users_data.get(str(ctx.author.id))
                target_name = f"User: @{str(ctx.author)}"
            else:
                guild_dict = self.bot.guilds_data.get(str(ctx.guild.id))
                if guild_dict is None:
                    return await ctx.send("サーバーの設定が存在しないため実行できません。")
                target_dict = guild_dict.get(str(ctx.author.id))
                if target_dict is None:
                    await self.bot.database.write_new_data(guild_dict, ctx.author.id)
                    target_dict = guild_dict.get(str(ctx.author.id))
                target_name = f"Member: @{str(ctx.author)}"
        m = await ctx.send(embed=await self.compose_set_em(target_dict, target_name))

        # check_funcs
        def check_val(m):
            if m.author == ctx.author and m.channel == ctx.channel:
                try:
                    val = int(m.content)
                except SyntaxError:
                    return False
                if val > 5:
                    return False
                return True
            return False

        def check_type(m):
            if m.author == ctx.author and m.channel == ctx.channel:
                try:
                    type = int(m.content)
                except SyntaxError:
                    return False
                if type > 1:
                    return False
                return True
            return False

        def check_col(m):
            if m.author == ctx.author and m.channel == ctx.channel:
                col = m.content.replace("0x", "").replace("#", "")
                if len(col) != 6:
                    return False
                try:
                    if int(col, 16) > int("ffffff", 16):
                        return False
                except ValueError:
                    return False
                return True
            return False

        def check_id(m):
            if m.author == ctx.author and m.channel == ctx.channel:
                try:
                    str_id = str(m.content)
                except SyntaxError:
                    return False
                if len(str_id) != 18:
                    return False
                return True
            return False

        # 設定ループ
        while True:
            num = await self.bot.wait_for("message", timeout=15, check=check_val)

            if int(num.content) == 0:
                await m.edit(content="終了")
                await num.add_reaction("\U00002705")
                break

            elif int(num.content) == 1:
                if target_dict.get("hidden"):
                    target_dict["hidden"] = False
                else:
                    target_dict["hidden"] = True

            elif int(num.content) == 2:
                if target_dict.get("anonymity"):
                    target_dict["anonymity"] = False
                else:
                    target_dict["anonymity"] = True

            elif int(num.content) == 3:
                s = await ctx.send("embed_typeを送信してください。(1~1)")
                embed_type = await self.bot.wait_for(
                    "message", timeout=15, check=check_type
                )
                target_dict["embed_type"] = int(embed_type.content)
                try:
                    await embed_type.delete()
                except Exception:
                    pass
                await s.delete()

            elif int(num.content) == 4:
                s = await ctx.send("embed_colorを16進数で送信してください。")
                embed_color = await self.bot.wait_for(
                    "message", timeout=15, check=check_col
                )
                target_dict["embed_color"] = embed_color.content.replace(
                    "0x", ""
                ).replace("#", "")
                try:
                    await embed_color.delete()
                except Exception:
                    pass
                await s.delete()

            elif int(num.content) == 5:
                s = await ctx.send("引用を許可する場所、アカウントのIDを送信してください。")
                allow_num = await self.bot.wait_for("message", check=check_id)
                if int(allow_num.content) not in target_dict.get("allow"):
                    target_dict["allow"].append(int(allow_num.content))
                else:
                    target_dict["allow"].remove(int(allow_num.content))
                try:
                    await allow_num.delete()
                except Exception:
                    pass
                await s.delete()

            try:
                await num.delete()
            except Exception:
                await num.add_reaction("\U00002705")
            await m.edit(embed=await self.compose_set_em(target_dict, target_name))
        # 終了時
        await self.bot.database.write_all_data(self.bot)


def setup(bot):
    bot.add_cog(Set(bot))
