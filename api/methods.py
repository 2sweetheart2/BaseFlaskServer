from abc import ABCMeta, abstractmethod

from api.objects import User
from api.params import *


# this class allows you to use the methods for all
class Method(metaclass=ABCMeta):
    name = None

    @property
    def params(self):
        return []

    @property
    def optional_params(self):
        return []

    @abstractmethod
    def _process(self, **kwargs):
        pass

    def process(self, **kwargs):
        self.check_arguments(kwargs)
        return self._process(**kwargs)

    def check_arguments(self, params):

        for param in self.params:
            if param.name not in params:
                raise MissingRequiredArgument(param.name)
            params[param.name] = param.validate(params[param.name])
        for param in self.optional_params:
            if param.name in params:
                params[param.name] = param.validate(params[param.name])


# this class allows you to use the method only for authorized users (you can change the logic for yourself)
class AuthorizedMethod(Method, metaclass=ABCMeta):
    def __init__(self):
        self.user = None

    @property
    def params(self):
        return []

    @abstractmethod
    def _process(self, **kwargs):
        pass

    def process(self, **kwargs):
        try:
            token = kwargs.pop('token')
        except KeyError:
            raise MissingRequiredArgument('token')
        self.user = User.authorize_by_token(token)
        self.check_arguments(kwargs)
        return self._process(**kwargs)


class MyMethod(Method):
    name = 'my_method'

    @property
    def params(self):
        # if you need some params in you method, you can add him
        return [String('info', True)]

    def _process(self, **kwargs):
        return {'your_info': kwargs.get('info')}
