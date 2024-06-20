from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Memes(Base):
    """
    Модель базы данных для хранения информации о мемах.

    Args:
        id (int): Уникальный идентификатор мема.
        name (str): Имя файла мема.
        description (str): Описание мема.
    """
    __tablename__ = 'memes'

    id = Column(Integer, primary_key=True)
    name = Column(String(length=64))
    description = Column(String(length=255))
