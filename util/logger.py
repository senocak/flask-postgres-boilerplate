import logging
from settings import app


level = logging.WARNING

if app.config.get('DEBUG'):
    level = logging.DEBUG

logging.basicConfig(level=level)
logger = logging.getLogger('api.log')
