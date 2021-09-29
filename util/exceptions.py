from http import HTTPStatus
from util.logger import logger


class AppException(Exception):
    status_code = HTTPStatus.BAD_REQUEST.real

    def __init__(self, messages, status_code=HTTPStatus.NOT_FOUND.real):
        Exception.__init__(self)
        self.messages = messages if isinstance(messages, list) else [messages]

        if status_code is not None:
            self.status_code = status_code

        logger.info('App Exception: %s', messages)

    def to_dict(self):
        return {'success': False, 'messages': self.messages}
