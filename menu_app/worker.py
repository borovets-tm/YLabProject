"""Модуль инициализации и конфигурирования Celery."""
from celery import Celery
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from menu_app.config import config

celery = Celery('menu_app', include=['menu_app.tasks'])
celery.conf.broker_url = config.broker_url
celery.conf.beat_schedule = {
    'run-me-every-fifteen-seconds': {
        'task': 'menu_app.tasks.update_db_from_excel',
        'schedule': 15.0,
    }
}
sync_engine = create_engine(config.sync_sqlalchemy_url, echo=True)
SyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=sync_engine,
)
