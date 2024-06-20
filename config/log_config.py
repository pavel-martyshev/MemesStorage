import os
import sys
import logging
import logging.config
import traceback
from logging.handlers import TimedRotatingFileHandler

from icecream import install
from environs import Env

# Инициализация переменных окружения
env = Env()
env.read_env()

# Установка icecream для удобной отладки
install()

# Установка директории для логов
logs_dir = os.path.join(os.path.dirname(__file__), '../' 'logs')
if not os.path.exists(logs_dir):
    os.mkdir(logs_dir)

# Определение файла для логов
filename = os.path.join(logs_dir, 'logs.log')

# Установка уровня логирования
LOG_LEVEL = env('LOG_LEVEL')
LOG_LEVEL = getattr(logging, LOG_LEVEL)

# Настройка логгера
logger = logging.getLogger()
logger.setLevel(LOG_LEVEL)

# Форматтер для логов
file_formatter = logging.Formatter('%(asctime)s | %(funcName)s | %(levelname)s | %(message)s',
                                   datefmt='%H:%M:%S')

# Обработчик логов с ротацией файлов
log_file_handler = TimedRotatingFileHandler(filename=filename, when='midnight', interval=1,
                                            encoding='utf-8', backupCount=50)
log_file_handler.suffix = "%d-%m-%Y"
log_file_handler.setFormatter(file_formatter)

# Добавление обработчика к логгеру
logger.addHandler(log_file_handler)


def exception_handler(exc_type, exc_value, exc_traceback):
    """
    Обработчик исключений для логирования неожиданных ошибок.

    Args:
        exc_type (type): Тип исключения.
        exc_value (Exception): Значение исключения.
        exc_traceback (traceback): Трассировка стека исключения.

    Returns:
        None
    """
    if exc_type.__name__ == 'KeyboardInterrupt':
        return
    tb_str = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    logging.error('\n%s', tb_str)


# Установка обработчика исключений в системе
sys.excepthook = exception_handler
