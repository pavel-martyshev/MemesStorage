import io
from typing import List

from fastapi import UploadFile, HTTPException
from marshmallow import ValidationError

from app.validators.validators import FileSchema
from database.core import session
from database.models import Memes
from storage.core import client
from database.CRUD import add_item, get_item, update_item, delete_item
from config import app_config

file_schema = FileSchema()


async def get_objects_urls(page: int) -> List[str]:
    """
    Асинхронная функция для получения URL-адресов объектов в хранилище с поддержкой пагинации.

    Args:
        page (int): Номер страницы для пагинации.

    Returns:
        List[str]: Список URL-адресов объектов в хранилище.
    """
    objects = client.list_objects('memes-storage')
    urls = []
    start_index = (page - 1) * app_config.app.page_size
    end_index = start_index + app_config.app.page_size

    for i, obj in enumerate(objects):
        if i < start_index:
            continue
        if i >= end_index:
            break
        urls.append(client.presigned_get_object('memes-storage', obj.object_name))

    return urls


async def save_file(file: UploadFile, description: str, file_id=None):
    """
    Асинхронная функция для сохранения файла в хранилище и базу данных.

    Args:
        file (UploadFile): Загружаемый файл.
        description (str): Описание файла.
        file_id (int, optional): Идентификатор файла для обновления, если файл уже существует.

    Exception:
        HTTPException: Если данные файла не прошли валидацию или возникли проблемы при сохранении.

    Returns:
        None
    """
    filename = file.filename

    validate_data = {
        'filename': filename,
        'content_type': file.content_type,
        'size': file.size
    }

    try:
        file_schema.load(validate_data)
    except ValidationError as err:
        raise HTTPException(status_code=400, detail=err.messages)

    data = {'name': filename, 'description': description}

    if file_id:
        old_file = await get_item(session, Memes, **{'id': file_id})
        request_res = await update_item(session, Memes, file_id, **data)

        if old_file.name != filename:
            client.remove_object('memes-storage', old_file.name)
    else:
        request_res = await add_item(session, Memes, **data)

    if isinstance(request_res, bool):
        file_bytes = file.file.read()
        client.put_object('memes-storage', filename, io.BytesIO(file_bytes),
                          length=len(file_bytes), content_type=file.content_type)
    else:
        raise HTTPException(status_code=400, detail=request_res)


async def get_file(file_id: int) -> str:
    """
    Асинхронная функция для получения URL-адреса файла по его идентификатору.

    Args:
        file_id (int): Идентификатор файла.

    Exception:
        HTTPException: Если файл не найден.

    Returns:
        str: URL-адрес файла.
    """
    file = await get_item(session, Memes, **{'id': file_id})

    if file:
        return client.presigned_get_object('memes-storage', file.name)
    raise HTTPException(status_code=400, detail='File not found')


async def delete_file(file_id: int):
    """
    Асинхронная функция для удаления файла из хранилища и базы данных по его идентификатору.

    Args:
        file_id (int): Идентификатор файла.

    Exception:
        HTTPException: Если возникли проблемы при удалении файла.

    Returns:
        None
    """
    request_res = await delete_item(session, Memes, file_id)

    if isinstance(request_res, Memes):
        client.remove_object('memes-storage', request_res.name)
    else:
        raise HTTPException(status_code=400, detail=request_res)
