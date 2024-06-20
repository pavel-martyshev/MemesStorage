from dataclasses import dataclass
from typing import List

from environs import Env


@dataclass
class App:
    """
    Класс для конфигурации приложения.

    Args:
        allowed_file_types (List): Список допустимых типов файлов.
        max_file_size (int): Максимально допустимый размер файла в байтах.
        page_size (int): Размер страницы для пагинации.
    """
    allowed_file_types: List
    max_file_size: int
    page_size: int


@dataclass
class Storage:
    """
    Класс для конфигурации хранилища.

    Args:
        endpoint (str): Адрес хранилища.
        access_key (str): Ключ доступа.
        secret_key (str): Секретный ключ.
        secure (bool): Использование безопасного соединения.
    """
    endpoint: str
    access_key: str
    secret_key: str
    secure: bool


@dataclass
class Database:
    """
    Класс для конфигурации базы данных.

    Args:
        db_host (str): Хост базы данных.
        db_port (str): Порт базы данных.
        db_name (str): Имя базы данных.
        db_user (str): Имя пользователя базы данных.
        db_password (str): Пароль пользователя базы данных.
    """
    db_host: str
    db_port: str
    db_name: str
    db_user: str
    db_password: str


@dataclass
class Config:
    """
    Класс для общей конфигурации приложения.

    Args:
        app (App): Конфигурация приложения.
        storage (Storage): Конфигурация хранилища.
        db (Database): Конфигурация базы данных.
    """
    app: App
    storage: Storage
    db: Database


def load_config() -> Config:
    """
    Загружает конфигурацию из переменных окружения.

    Returns:
        Config: Конфигурация приложения, хранилища и базы данных.
    """
    env = Env()
    env.read_env()
    storage_endpoint = f'{env("STORAGE_HOST")}:{env("STORAGE_PORT")}'

    allowed_file_types = env('ALLOWED_FILE_TYPES').split(',')
    max_file_size = int(env('MAX_FILE_SIZE')) * 1024 * 1024

    return Config(
        app=App(allowed_file_types=allowed_file_types, max_file_size=max_file_size,
                page_size=int(env('PAGE_SIZE'))),
        storage=Storage(endpoint=storage_endpoint,
                        access_key=env('ACCESS_KEY'),
                        secret_key=env('SECRET_KEY'),
                        secure=bool(int(env('SECURE')))),
        db=Database(db_host=env("DB_HOST"),
                    db_port=env("DB_PORT"),
                    db_name=env("DB_NAME"),
                    db_user=env("DB_USER"),
                    db_password=env("DB_PASSWORD")),
    )
