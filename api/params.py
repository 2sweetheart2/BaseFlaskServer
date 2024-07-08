"""
this file needed for create types of needed params in methods
"""
from api.api_exceptions import *


class Param:
    def __init__(self, _type, name, has_to_be_truthy=False, not_null=True):
        self.type = _type
        self.name = name
        self.not_null = not_null
        self.truthy = has_to_be_truthy

    @property
    def custom_checks(self):
        return []

    def validate(self, value):
        if not isinstance(value, self.type):
            try:
                value = self.type(value)
            except ValueError:
                raise BadArgumentType(self.name)
        elif self.truthy and not value:
            raise BadArgument(self.name)
        if self.not_null and value == "None":
            raise BadArgumentType(f'{self.name}. (can\'t be null)')
        for check in self.custom_checks:
            res = check(value)
            if res:
                value = res
        return value


class String(Param):
    def __init__(self, name, has_to_be_truthy=False, max_length=0, min_lenght=0, not_null=True):
        self.max_length = max_length
        self.min_length = min_lenght
        self.not_null = not_null
        super().__init__(str, name, has_to_be_truthy, not_null)

    def length_check(self, value):
        if not self.not_null:
            return
        if self.max_length and len(value) > self.max_length:
            raise CustomBadArgument(f'Invalid argument: {{}}. Argument length exceeds {self.max_length}.', self.name)
        if self.min_length and len(value) < self.min_length:
            raise CustomBadArgument(f'Invalid argument: {{}}. Argument length exceeds {self.min_length}.', self.name)

    @staticmethod
    def strip_check(value):
        return value.strip()

    @property
    def custom_checks(self):
        return [self.length_check, self.strip_check]
