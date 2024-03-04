"""
Connect to database according to settings 
"""

from config import settings


async def database_connect() -> object:
    """
    Connect to database according to settings
    Args:
        None
    Returns:
        connection object
    """
    if settings.DB_TYPE == "sqlite":
        import aiosqlite as asql

        return await asql.connect(settings.SQLITE_DB_PATH, check_same_thread=False)
    elif settings.DB_TYPE == "mysql":
        import aiomysql

        return await aiomysql.connect(**settings.MYSQL_DB_SEETINGS, autocommit=True)
    elif settings.DB_TYPE == "postgres":
        import asyncpg

        return await asyncpg.connect(**settings.POSTGRES_DB_SEETINGS, autocommit=True)
    else:
        raise ValueError("Неизвестный тип базы данных")
