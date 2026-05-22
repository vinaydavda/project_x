# Running this file initiates tables in database

import time
import logging
from app.db.postgres import engine, Base
from app.models.events import Event

_logger = logging.getLogger(__name__)

def create_tables():
    while True:
        try:
            Base.metadata.create_all(bind=engine)
            _logger.info(f"> [CREATE TABLE] - DB Tables created successfully")
            break
        except Exception as e:
            _logger.error(f"> [CREATE TABLE] - Error creating DB tables, retrying...: {e}")
            time.sleep(5)