from enum import Enum


class DbBackend(str, Enum):
    POSTGRESQL = "postgresql"
    MYSQL = "mysql"
