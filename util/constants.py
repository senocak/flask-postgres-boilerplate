from enum import Enum, unique


@unique
class Roles(Enum):
    admin = 'ROLE_ADMIN'
    user = 'ROLE_USER'

    @staticmethod
    def list():
        return list(map(lambda c: c.value, Roles))
