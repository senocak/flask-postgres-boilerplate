from enum import Enum, unique


@unique
class Roles(Enum):
    admin = 'ADMIN'
    user = 'USER'

    @staticmethod
    def list():
        return list(map(lambda c: c.value, Roles))
