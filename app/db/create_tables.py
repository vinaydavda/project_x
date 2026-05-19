# Running this file initiates tables in database

import logging
from app.db.postgres import engine, Base
from app.models.events import Event

_logger = logging.getLogger(__name__)

try:
    Base.metadata.create_all(bind=engine)
    _logger.info(f"> [INFO] - DB Tables created successfully")
except Exception as e:
    _logger.error(f"> [ERROR] - Error creating DB tables")