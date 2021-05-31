import asyncio
import discord
from discord.ext import commands
from discord_slash import SlashContext, cog_ext
from discord_slash.utils.manage_commands import create_choice, create_option


class Set(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        asyncio.create_task(self.bot.slash.sync_all_commands())
        self.timeout = discord.Embed(title='ERROR', description='タイムアウトしました。')

    def cog_unload(self):
        self.bot.slash.remove_cog_commands(self)

    async def compose_set_em(self, target_dict, target_name):
        embed = discord.Embed(
            title=target_name,
            description='設定する項目を番号で選択してください。\n0: 終了',
            color=target_dict.get("embed_color")
        )
        embed.add_field(
            name='1: hidden',
            value=f'```\n{target_dict.get("hidden")}\n```'
        )
        embed.add_field(
            name='2: anonymity',
            value=f'```\n{target_dict.get("anonymity")}\n```'
        )
        embed.add_field(
            name='3: embed_type',
            value=f'```\n{target_dict.get("embed_type")}\n```'
        )
        embed.add_field(
            name='4: embed_color',
            value=f'```\n{target_dict.get("embed_color")}\n```'
        )
        embed.add_field(
            name='5: allow',
            value=f'```\n{target_dict.get("allow")}\n```'
        )
        return embed

    @cog_ext.cog_slash(
        name='set',
        description='展開に関する設定',
        options=[
            create_option(
                name='target',
                description='設定する対象を選択',
                option_type=4, required=True,
                choices=[
                    create_choice(name='server', value=1),
                    create_choice(name='user', value=2)
                ]
            )
        ]
    )
    async def slash_say(self, ctx: SlashContext, target, category=None, role=None, channel=None):
        if await self.bot.Check.com_per(ctx, target) is False:
            return
        if target == 1:
            target_dict = self.bot.guilds_data.get(str(ctx.guild.id))
            if target_dict is None:
                await self.bot.database.write_new_data(self.bot.guilds_data, ctx.guild.id)
                target_dict = self.bot.guilds_data.get(str(ctx.guild.id))
            target_name = f'Server: {ctx.guild.name}'
        if target == 2:
            target_dict = self.bot.users_data.get(str(ctx.author.id))
            if target_dict is None:
                await self.bot.database.write_new_data(self.bot.users_data, ctx.author.id)
                target_dict = self.bot.users_data.get(str(ctx.author.id))
            target_name = f'User: @{str(ctx.author)}'
        m = await ctx.send(embed=await self.compose_set_em(target_dict, target_name))
        while True:
            def check_int(m):
                if m.author == ctx.author and m.channel == ctx.channel:
                    try:
                        num = int(m.content)
                    except SyntaxError:
                        return False
                    if num > 5:
                        return False
                    return True
                else:
                    return False

            try:
                num = await self.bot.wait_for('message', timeout=60, check=check_int)
            except asyncio.TimeoutError:
                return await m.edit(embed=self.timeout)
            if int(num.content) == 0:
                await m.edit(content='終了', embed=None)
                await num.add_reaction('\U00002705')
                break
            elif int(num.content) == 1:
                if target_dict.get('hidden'):
                    target_dict["hidden"] = False
                else:
                    target_dict["hidden"] = True
            elif int(num.content) == 2:
                if target_dict.get('anonymity'):
                    target_dict["anonymity"] = False
                else:
                    target_dict["anonymity"] = True
            elif int(num.content) == 3:
                s = await ctx.send('embed_typeを送信してください。(1~1)')
                try:
                    embed_type = await self.bot.wait_for('message', timeout=60, check=check_int)
                except asyncio.TimeoutError:
                    return await m.edit(embed=self.timeout)
                target_dict["embed_type"] = int(embed_type.content)
                try:
                    await embed_type.delete()
                except Exception:
                    pass
                await s.delete()
            elif int(num.content) == 4:
                s = await ctx.send('embed_colorを16進数で送信してください。')
                try:
                    embed_color = await self.bot.wait_for('message', timeout=60, check=check_int)
                except asyncio.TimeoutError:
                    return await m.edit(embed=self.timeout)
                target_dict["embed_color"] = int(embed_color.content)
                try:
                    await embed_color.delete()
                except Exception:
                    pass
                await s.delete()
            elif int(num.content) == 5:
                s = await ctx.send('引用を許可する場所、アカウントのIDを送信してください。')
                try:
                    allow_num = await self.bot.wait_for('message', timeout=60, check=check_int)
                except asyncio.TimeoutError:
                    return await m.edit(embed=self.timeout)
                if int(allow_num.content) not in target_dict.get('allow'):
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
                await num.add_reaction('\U00002705')
            await m.edit(embed=await self.compose_set_em(target_dict, target_name))
        await self.bot.database.write_all_data(self.bot)


def setup(bot):
    bot.add_cog(Set(bot))
