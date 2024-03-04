"""
Database manager 
"""

import logging
from config import settings

from utils.logger import (
    handle_exceptions,
)  # Декоратор, который перехватывает исключения


class DataManager:
    def __init__(self, path: str) -> None:
        """
        Initializes the class with the given path.

        Args:
            path (str): The path to be initialized.

        Returns:
            None
        """
        self.path = path

    @staticmethod
    @handle_exceptions
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

            return await aiomysql.connect(
                **settings.MYSQL_DB_SEETINGS, autocommit=settings.DB_AUTOCOMMIT
            )
        elif settings.DB_TYPE == "postgres":
            import asyncpg

            return await asyncpg.connect(
                **settings.POSTGRES_DB_SEETINGS, autocommit=settings.DB_AUTOCOMMIT
            )
        else:
            raise ValueError(f"Unsupported database type: {settings.DB_TYPE}")

    # Оставлен на будущее, если придётся использовать логгирование внутри
    def log_error(self, message: str) -> None:
        """
        Logs an error message to a specified file and the default logging system.

        Args:
            self: The object instance
            message (str): The error message to be logged

        Returns:
            None
        """
        logging.error(message)


class SQLDataManager(DataManager):
    """
    Класс для управления SQL базой данных, обеспечивающий асинхронное подключение,
    выполнение запросов и управление транзакциями.

    Attributes:
        path (str): Путь к файлу базы данных или параметры соединения.
        connection (object): Асинхронное соединение с базой данных.
    """

    def __init__(self, path: str) -> None:
        """
        Инициализирует экземпляр класса SQLDataManager с заданным путём.

        Args:
            path (str): Путь к файлу базы данных или параметры соединения.
        """
        super().__init__(path)
        self.connection = None

    @handle_exceptions
    async def connect(self) -> None:
        """
        Асинхронно устанавливает соединение с базой данных в соответствии с настройками.
        """
        self.connection = await super().database_connect()

    @handle_exceptions
    async def close(self) -> None:
        """
        Асинхронно закрывает соединение с базой данных, если оно было установлено.
        """
        if self.connection:
            await self.connection.close()

    @handle_exceptions
    async def start_transaction(self) -> None:
        """
        Асинхронно начинает транзакцию в текущем соединении с базой данных.
        """
        if not self.connection:
            raise ValueError("Соединение с базой данных не установлено.")
        self.transaction = self.connection.transaction()
        await self.transaction.start()

    @handle_exceptions
    async def commit_transaction(self) -> None:
        """
        Асинхронно подтверждает (коммитит) текущую транзакцию в соединении с базой данных.
        """
        if not self.connection:
            raise ValueError("Соединение с базой данных не установлено.")
        await self.transaction.commit()

    @handle_exceptions
    async def rollback_transaction(self) -> None:
        """
        Асинхронно откатывает текущую транзакцию в соединении с базой данных.
        """
        if not self.connection:
            raise ValueError("Соединение с базой данных не установлено.")
        await self.transaction.rollback()

    @handle_exceptions
    async def commit_or_rollback_params_transaction(
        self, query: str, params: tuple | None
    ) -> None:
        """
        Асинхронно подтверждает (коммитит) или откатывает текущую транзакцию в соединении с базой данных в зависимости от успешности выполнения запроса.
        """
        if not self.connection:
            raise ValueError("Соединение с базой данных не установлено.")
        try:
            await self.start_transaction()
            result = await self.connection.execute(query, params)
            await self.transaction.commit()
            return result
        except Exception as e:
            await self.transaction.rollback()
            raise e

    @handle_exceptions
    async def execute_query_with_params(self, query: str, params: tuple) -> None:
        """
        Асинхронно выполняет SQL-запрос с параметрами в текущем соединении с базой данных.

        Args:
            query (str): SQL-запрос для выполнения.
            params (tuple): Параметры для подстановки в SQL-запрос.
        """
        if not self.connection:
            raise ValueError("Соединение с базой данных не установлено.")
        return await self.connection.execute(query, params)

    @handle_exceptions
    async def execute_query(self, query: str) -> None:
        """
        Асинхронно выполняет SQL-запрос в текущем соединении с базой данных.

        Args:
            query (str): SQL-запрос для выполнения.
        """
        if not self.connection:
            raise ValueError("Соединение с базой данных не установлено.")
        await self.connection.execute(query)

    @handle_exceptions
    async def commit(self) -> None:
        """
        Асинхронно коммитит изменения.
        """
        if not self.connection:
            raise ValueError("Соединение с базой данных не установлено.")
        await self.connection.commit()
