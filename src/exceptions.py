class UserAlreadyExistsError(Exception):
    _msg = 'User with this credentials already exists!'

    def __init__(self, msg=None):
        self.msg = UserAlreadyExistsError._msg
        if msg:
            self.msg = msg
