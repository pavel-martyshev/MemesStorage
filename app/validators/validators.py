from marshmallow import Schema, fields, ValidationError, validates

from database.core import session
from database.models import Memes

from config import app_config

ALLOWED_FILE_TYPES = app_config.app.allowed_file_types
MAX_FILE_SIZE = app_config.app.max_file_size


class FileSchema(Schema):
    """
    Схема для валидации файловых данных с использованием Marshmallow.

    Args:
        filename (fields.Str): Имя файла (обязательно).
        content_type (fields.Str): Тип содержимого файла (обязательно).
        size (fields.Int): Размер файла в байтах (обязательно).

    Methods:
        validate_filename(value): Проверяет, существует ли файл с таким же именем в базе данных.
        validate_content_type(value): Проверяет, является ли тип содержимого допустимым.
        validate_size(value): Проверяет, не превышает ли размер файла максимально допустимый размер.
    """
    filename = fields.Str(required=True)
    content_type = fields.Str(required=True)
    size = fields.Int(required=True)

    @validates('filename')
    def validate_filename(self, value):
        """
        Проверяет, существует ли файл с таким же именем в базе данных.

        Args:
            value (str): Имя файла.

        Exceptions:
            ValidationError: Если файл с таким именем уже существует.
        """
        meme = session.query(Memes).filter(Memes.name == value).one_or_none()
        if meme:
            raise ValidationError('A meme with the same name already exists')

    @validates('content_type')
    def validate_content_type(self, value):
        """
        Проверяет, является ли тип содержимого допустимым.

        Args:
            value (str): Тип содержимого файла.

        Exceptions:
            ValidationError: Если тип содержимого файла недопустим.
        """
        if value not in ALLOWED_FILE_TYPES:
            raise ValidationError('Invalid file type')

    @validates('size')
    def validate_size(self, value):
        """
        Проверяет, не превышает ли размер файла максимально допустимый размер.

        Args:
            value (int): Размер файла в байтах.

        Exceptions:
            ValidationError: Если размер файла превышает максимально допустимый.
        """
        if value > MAX_FILE_SIZE:
            raise ValidationError('File too big')
