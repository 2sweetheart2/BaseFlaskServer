"""
this file is for describing all possible errors when working with the api
"""


class InvalidRequest(Exception):
    code = 0
    string = 'invalid_request'
    message = 'Invalid request.'


class InvalidMethod(InvalidRequest):
    code = 1
    string = 'invalid_method'
    message = 'No such method found.'


class ArgumentsError(InvalidRequest):
    code = 2
    string = 'invalid_arguments'
    message = 'Invalid arguments.'


class CustomBadArgument(ArgumentsError):
    code = 3
    string = 'invalid_argument'

    def __init__(self, message, arg):
        self._message = message
        self.arg = arg

    @property
    def message(self):
        return self._message.format(self.arg)


class BadArgument(CustomBadArgument):
    def __init__(self, arg):
        super().__init__('Invalid argument: {}', arg)


class MissingRequiredArgument(CustomBadArgument):
    code = 4
    string = 'missing_argument'

    def __init__(self, arg):
        super().__init__('Missing required argument: {}', arg)


class BadArgumentType(CustomBadArgument):
    code = 5
    string = 'invalid_argument_type'

    def __init__(self, arg):
        super().__init__('Invalid argument type for argument: {}', arg)


class InvalidTokenError(BadArgument):
    code = 6
    string = 'invalid_token'
    message = 'Invalid token.'

    def __init__(self):
        pass


class UserDoesNotExist(ArgumentsError):
    code = 7
    string = 'user_does_not_exist'
    message = 'User with such email address does not exist.'


class UserNotFound(CustomBadArgument):
    code = 8
    string = 'user_not_found'

    def __init__(self, arg):
        super().__init__('User with id {} was not found.', arg)


class WrongPassword(ArgumentsError):
    code = 9
    string = 'wrong_password'
    message = 'Invalid password.'


class BadEmail(CustomBadArgument):
    code = 10
    string = 'invalid_email'

    def __init__(self, arg):
        super().__init__('Invalid email: "{}".', arg)
