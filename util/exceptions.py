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


class ContentNotFound(AppException):
    def __init__(self):
        AppException.__init__(self, 'İçerik bulunamadı!', HTTPStatus.NOT_FOUND.real)


class FileNotFound(AppException):
    def __init__(self):
        AppException.__init__(self, 'Dosya bulunamadı!', HTTPStatus.NOT_FOUND.real)


class UserNotFound(AppException):
    def __init__(self):
        AppException.__init__(self, 'Böyle bir kullanıcı bulunmamaktadır!', HTTPStatus.NOT_FOUND.real)


class UserNotDefined(AppException):
    def __init__(self):
        error_msg = "There is no global user value. " \
                    "Make sure to use @get_current_user decorator."
        AppException.__init__(self, error_msg, HTTPStatus.INTERNAL_SERVER_ERROR.real)


class AuthException(AppException):
    def __init__(self):
        AppException.__init__(self, 'Kullanıcı adı ya da şifre hatalıdır')


class InvalidJWTException(AppException):
    def __init__(self):
        AppException.__init__(self, 'User data in JWT is not valid')


class MalformedJWTException(AppException):
    def __init__(self):
        AppException.__init__(self, 'Provided JWT is not malformed!!')


class UnauthorizedException(AppException):
    def __init__(self):
        AppException.__init__(self, 'Unauthorized', HTTPStatus.FORBIDDEN.real)


class UserRolesPermission(AppException):
    def __init__(self):
        AppException.__init__(self, 'User Permission')


class UserQuotaExpire(AppException):
    def __init__(self):
        AppException.__init__(self, 'User Quota Limit')


class EmailCodeException(AppException):
    def __init__(self):
        AppException.__init__(self, 'Email doğrulama kodu geçerli değildir.', HTTPStatus.BAD_REQUEST.real)


class UserDeactivateException(AppException):
    def __init__(self):
        AppException.__init__(self, 'Kullanıcı aktif değil.', HTTPStatus.BAD_REQUEST.real)


class PasswordException(AppException):
    def __init__(self):
        AppException.__init__(self,
                              'Şifre en az 1 nümerik, birer büyük-küçük harf içermeli ve en az 6 haneden oluşmalıdır.',
                              HTTPStatus.BAD_REQUEST.real)
