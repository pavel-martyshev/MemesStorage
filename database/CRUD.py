from typing import TypeVar, Union, Any

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

T = TypeVar('T')


async def add_item(session: Session, model: T, **kwargs) -> Union[str, bool]:
    """
    Асинхронная функция для добавления элемента в базу данных.

    Args:
        session (Session): Сессия SQLAlchemy.
        model (T): Модель SQLAlchemy, представляющая таблицу базы данных.
        **kwargs: Поля модели и их значения.

    Returns:
        bool или str: True, если операция успешна, иначе сообщение об ошибке.
    """
    try:
        session.add(model(**kwargs))
        session.commit()
        session.close()
    except SQLAlchemyError as err:
        return f'{err}'
    return True


async def get_item(session: Session, model: T, **kwargs) -> Any:
    """
    Асинхронная функция для получения элемента из базы данных.

    Args:
        session (Session): Сессия SQLAlchemy.
        model (T): Модель SQLAlchemy, представляющая таблицу базы данных.
        **kwargs: Условия фильтрации для поиска элемента.

    Returns:
        Any: Найденный элемент или None, если элемент не найден.
    """
    query = session.query(model)

    for key, value in kwargs.items():
        query = query.filter(getattr(model, key) == value)

    result = query.one_or_none()
    session.close()

    return result


async def update_item(session: Session, model: T, item_id: int, **kwargs) -> Union[str, bool]:
    """
    Асинхронная функция для обновления элемента в базе данных.

    Args:
        session (Session): Сессия SQLAlchemy.
        model (T): Модель SQLAlchemy, представляющая таблицу базы данных.
        item_id (int): Идентификатор элемента для обновления.
        **kwargs: Поля модели и их новые значения.

    Returns:
        bool или str: True, если операция успешна, иначе сообщение об ошибке.
    """
    with session.begin():
        item = session.query(model).filter(model.id == item_id).one_or_none()

        try:
            if item:
                for key, value in kwargs.items():
                    if hasattr(item, key):
                        setattr(item, key, value)
                session.commit()
        except SQLAlchemyError as err:
            return f'{err}'
        return True


async def delete_item(session: Session, model: T, item_id: int) -> Any:
    """
    Асинхронная функция для удаления элемента из базы данных.

    Args:
        session (Session): Сессия SQLAlchemy.
        model (T): Модель SQLAlchemy, представляющая таблицу базы данных.
        item_id (int): Идентификатор элемента для удаления.

    Returns:
        Any: Удалённый элемент или сообщение об ошибке.
    """
    with session.begin():
        try:
            item = session.query(model).filter(model.id == item_id).one_or_none()
            session.delete(item)
        except SQLAlchemyError as err:
            return f'{err}'
        return item
