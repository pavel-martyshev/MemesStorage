from minio import Minio

from config import app_config, logger

client = Minio(
    endpoint=app_config.storage.endpoint,
    access_key=app_config.storage.access_key,
    secret_key=app_config.storage.secret_key,
    secure=app_config.storage.secure
)


def load_storage(bucket_name: str):
    """
    Проверяет существование указанного бакета в хранилище Minio и создает его, если он не
    существует.

    Args:
        bucket_name (str): Имя бакета.

    Returns:
        None
    """
    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)
        logger.info(f'Bucket "{bucket_name}" created')
    else:
        logger.info(f'Bucket "{bucket_name}" exists')
