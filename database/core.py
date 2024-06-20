from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.models import Base
from config import app_config

DATABASE_URL = (f'postgresql://{app_config.db.db_user}:{app_config.db.db_password}@'
                f'{app_config.db.db_host}:{app_config.db.db_port}/{app_config.db.db_name}')
engine = create_engine(DATABASE_URL)

Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)


def create_models():
    Base.metadata.create_all(engine)
