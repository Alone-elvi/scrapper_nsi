"""
Settings module
"""
from datetime import datetime
from pathlib import Path
import sys

sys.path.append(Path(__file__).resolve().parent.parent / "config")
sys.path.append(Path(__file__).resolve().parent.parent / "database")
sys.path.append(Path(__file__).resolve().parent.parent / "excel")
sys.path.append(Path(__file__).resolve().parent.parent / "output")
sys.path.append(Path(__file__).resolve().parent.parent / "utils")
sys.path.append(Path(__file__).resolve().parent.parent / "parser")


# URL_NAME_PROD = "Биологическая+активная"
# URL_DATE = "2024-02-20"

# URL = f"https://nsi.eaeunion.org/portal/1995?NAME_PROD={URL_NAME_PROD}&date={URL_DATE}"

BASE_PATH = Path(__file__).resolve().parent.parent

# DB section settings

SQLITE_DB_NAME = "database.db"
SQLITE_DB_DIR = BASE_PATH / "storage"
SQLITE_DB_PATH = SQLITE_DB_DIR / SQLITE_DB_NAME

MYSQL_DB_NAME = "mysql"
MYSQL_DB_HOST = "localhost"
MYSQL_DB_USER = "root"
MYSQL_DB_PASS = "root"
MYSQL_DB_PORT = 3306


MYSQL_DB_SEETINGS = {
    "host": MYSQL_DB_HOST,
    "user": MYSQL_DB_USER,
    "password": MYSQL_DB_PASS,
    "database": MYSQL_DB_NAME,
    "port": MYSQL_DB_PORT
}

POSTGRES_DB_NAME = "postgres"
POSTGRES_DB_HOST = "localhost"
POSTGRES_DB_USER = "postgres"
POSTGRES_DB_PASS = "postgres"
POSTGRES_DB_PORT = 5432

POSTGRES_DB_SEETINGS = {
    "host": POSTGRES_DB_HOST,
    "user": POSTGRES_DB_USER,
    "password": POSTGRES_DB_PASS,
    "database": POSTGRES_DB_NAME,
    "port": POSTGRES_DB_PORT
}

DB_AUTOCOMMIT = False

DB_TYPE = "sqlite"

# Logging sections

LOGGING_LEVEL = "ERROR"
LOGGING_DIR = BASE_PATH / "logs"
LOGGING_FILE_ERROR = LOGGING_DIR / "error.log"
LOGGING_YES = True

# Parser section

PARSER_PARAMS = {
    "NAME_PROD": "Биологическая+активная", 
    "date": f"{datetime.now().strftime('%Y-%m-%d')}"
    }

PARSER_URL = f"""https://nsi.eaeunion.org/portal/1995?NAME_PROD={PARSER_PARAMS["NAME_PROD"]}&date={PARSER_PARAMS["date"]}"""