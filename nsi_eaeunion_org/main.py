"""
Main script
"""

import asyncio


from config import settings

from database import tables
from database.database import SQLDataManager
from utils import check_path, logger

from parser.parser import parser


async def main_parser() -> None:
    """
    main parser
    Args:
        None
    Returns:
        None
    """
    await parser()


async def main() -> None:
    """
    main
    Args:
        None
    Returns:
        None
    """
    check_path.check_path(settings.SQLITE_DB_DIR)
    logger.setup_logging()

    # при with получается 2-я загрузка потока
    db = SQLDataManager(settings.SQLITE_DB_PATH)
    await db.connect()
    print("connection -> ", db.connection)
    await db.execute_query(tables.CREATE_STATUS_TABLE)
    await db.execute_query(tables.FILL_STATUS_TABLE)
    await db.commit()
    await db.close()

    await main_parser()

if __name__ == "__main__":
    asyncio.run(main())
