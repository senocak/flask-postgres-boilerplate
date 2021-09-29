from model.user import User


def get_all():
    return User.query.all()


def getUserById(id):
    user = User.query.filter_by(id=id).first()
    return user
