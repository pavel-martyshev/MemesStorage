from typing import Optional

from fastapi import FastAPI, Request, UploadFile, Form
from fastapi.responses import JSONResponse

from database.core import create_models
from storage.core import load_storage
from .utils import save_file, get_file, delete_file, get_objects_urls

# Инициализация хранилища и базы данных
load_storage('memes-storage')
create_models()

app = FastAPI()


@app.api_route('/memes', methods=['GET', 'POST'])
async def memes_list(request: Request, description: Optional[str] = Form(None),
                     file: Optional[UploadFile] = None, page: int = 1) -> JSONResponse:
    """
    Получение списка мемов или загрузка нового мема.

    - **GET**: Возвращает список URL-адресов загруженных мемов.
    - **POST**: Загружает новый мем с описанием.

    Args:
        request (Request): HTTP запрос.
        description (Optional[str], Form): Описание мема.
        file (Optional[UploadFile]): Загружаемый файл мема.
        page (int): Номер страницы.

    Returns:
        JSONResponse: Сообщение об успехе загрузки или список URL-адресов мемов.
    """
    if request.method == 'POST':
        await save_file(file, description)
        return JSONResponse({'message': 'Success'}, status_code=200)

    urls = await get_objects_urls(page)
    return JSONResponse({'message': urls if urls else 'Memes not found'}, status_code=200)


@app.api_route('/memes/{meme_id}', methods=['GET', 'PUT', 'DELETE'])
async def meme_detail(request: Request, meme_id: int, description: Optional[str] = Form(None),
                      file: Optional[UploadFile] = None):
    """
    Получение, обновление или удаление мема по ID.

    - **GET**: Возвращает URL мема по заданному ID.
    - **PUT**: Обновляет мем по заданному ID.
    - **DELETE**: Удаляет мем по заданному ID.

    Args:
        request (Request): HTTP запрос.
        meme_id (int): ID мема.
        description (Optional[str], Form): Новое описание мема.
        file (Optional[UploadFile]): Новый файл мема.

    Returns:
        JSONResponse: Сообщение об успехе операции или URL мема.
    """
    if request.method == 'PUT':
        await save_file(file, description, meme_id)
        return JSONResponse({'message': 'Success'}, status_code=200)
    elif request.method == 'DELETE':
        await delete_file(meme_id)
        return JSONResponse({'message': 'Success'}, status_code=200)

    url = await get_file(meme_id)
    return JSONResponse({'message': url}, status_code=200)
