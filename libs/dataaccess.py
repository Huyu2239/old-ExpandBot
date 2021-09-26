import os
import asyncpg
from .enums import MutingTarget

DEFOLT_CONFIG = {"hidden": 1, "exception": "", "layout": 1, "color": 000000}


class UserConfigs:
    @staticmethod
    async def read(user_id):
        return DEFOLT_CONFIG
        conn = await asyncpg.connect(os.environ["SQL_TOKEN"])
        row = await conn.fetchrow(
            f"SELECT * FROM USER_CONFIGS WHERE user_id = {user_id};"
        )
        await conn.close()
        return row

    @staticmethod
    async def write(user_id, hidden, exception, layout, color):
        return
        conn = await asyncpg.connect(os.environ["SQL_TOKEN"])
        row = await conn.fetchrow(
            f"SELECT * FROM USER_CONFIGS WHERE user_id = {user_id};"
        )
        if row is None:
            await conn.execute(
                f"INSERT INTO USER_CONFIG VALUES ({user_id}, {hidden}, {exception}, {layout}, {color});"
            )
        else:
            await conn.execute(
                f"UPDATE USER_CONFIG SET hidden = '{hidden}', exception = '{exception}', layout = '{layout}', color = '{color}'  WHERE id = '{user_id}';"
            )
        return await conn.close()

    @staticmethod
    async def remove(user_id):
        return
        conn = await asyncpg.connect(os.environ["SQL_TOKEN"])
        await conn.execute(f"DELETE FROM USER_CONFIGS WHERE user_id = {user_id}")
        return await conn.close()


class MemberConfigs:
    @staticmethod
    async def read(member_id, guild_id):
        return DEFOLT_CONFIG
        conn = await asyncpg.connect(os.environ["SQL_TOKEN"])
        row = await conn.fetchrow(
            f"SELECT * FROM MEMBER_CONFIGS WHERE member_id = {member_id} and guild_id = {guild_id};"
        )
        await conn.close()
        return row

    @staticmethod
    async def write(member_id, guild_id, hidden, exception, layout, color):
        return
        conn = await asyncpg.connect(os.environ["SQL_TOKEN"])
        row = await conn.fetchrow(
            f"SELECT * FROM MEMBER_CONFIGS WHERE member_id = {member_id} and guild_id = {guild_id};"
        )
        if row is None:
            await conn.execute(
                f"INSERT INTO MEMBER_CONFIGS VALUES ({member_id}, {guild_id}, {hidden}, {exception}, {layout}, {color});"
            )
        else:
            await conn.execute(
                f"UPDATE MEMBER_CONFIGS SET hidden = '{hidden}', exception = '{exception}', layout = '{layout}', color = '{color}' WHERE member_id = '{member_id}' AND guild_id = '{guild_id}';"
            )
        return await conn.close()

    @staticmethod
    async def remove(member_id):
        return
        conn = await asyncpg.connect(os.environ["SQL_TOKEN"])
        await conn.execute(f"DELETE FROM MEMBER_CONFIGS WHERE member_id = {member_id}")
        return await conn.close()


class GuildConfigs:
    @staticmethod
    async def read(guild_id):
        return DEFOLT_CONFIG
        conn = await asyncpg.connect(os.environ["SQL_TOKEN"])
        row = await conn.fetchrow(f"SELECT * FROM GUILD_CONFIGS WHERE guild_id = {guild_id};")
        await conn.close()
        return row

    @staticmethod
    async def write(guild_id, hidden, exception, layout, color):
        return
        conn = await asyncpg.connect(os.environ["SQL_TOKEN"])
        row = await conn.fetchrow(
            f"SELECT * FROM GUILD_CONFIGS WHERE guild_id = {guild_id};"
        )
        if row is None:
            await conn.execute(
                f"INSERT INTO GUILD_CONFIGS VALUES ({guild_id}, {hidden}, {exception}, {layout}, {color});"
            )
        else:
            await conn.execute(
                f"UPDATE GUILD_CONFIGS SET hidden = '{hidden}', exception = '{exception}', layout = '{layout}', color = '{color}'  WHERE guild_id = '{guild_id}';"
            )
        return await conn.close()

    @staticmethod
    async def remove(guild_id):
        return
        conn = await asyncpg.connect(os.environ["SQL_TOKEN"])
        await conn.execute(f"DELETE FROM GUILD_CONFIGS WHERE guild_id = {guild_id}")
        return await conn.close()


class MuteConfigs:
    @staticmethod
    async def read(target_id, target_type):
        return False
        conn = await asyncpg.connect(os.environ["SQL_TOKEN"])
        row = await conn.fetch(f"SELECT * FROM MUTE_CONFIGS WHERE target_id = {target_id} AND target_type = {target_type.value};")
        return row is True

    @staticmethod
    async def add(target_id, target_type: MutingTarget):
        return
        conn = await asyncpg.connect(os.environ["SQL_TOKEN"])
        await conn.execute(
            f"INSERT INTO MUTE_CONFIG VALUES ({target_id}, {target_type.value});"
        )
        return await conn.close()

    @staticmethod
    async def remove(target_id):
        return
        conn = await asyncpg.connect(os.environ["SQL_TOKEN"])
        await conn.execute(f"DELETE FROM USER_CONFIGS WHERE target_id = {target_id}")
        return await conn.close()
