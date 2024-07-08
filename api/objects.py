"""
there you can create your object like User object and etc.
"""
from api.api_exceptions import *
from api.ctypto import verify_hashed_string
from api.sql_stuff import *


class User:
    def __init__(self, payload):
        self.id = payload.get('id')
        self.first_name = payload.get('first_name')
        self.last_name = payload.get('last_name')
        self.email = payload.get('email')
        self.password = payload.get('password')

    @classmethod
    def get(cls, user_id=None):
        res = sql_req('SELECT * FROM `users` WHERE id=%s', user_id if user_id is not None else None, fetch_one=True)
        if not res:
            raise UserNotFound(user_id)
        return cls(res)

    @classmethod
    def authorize(cls, email, password):
        res = sql_req('SELECT * FROM `users` WHERE email=%s', email, fetch_one=True)
        if not res:
            raise UserDoesNotExist
        if not verify_hashed_string(password, res.get('password')):
            raise WrongPassword
        user = cls(res)
        return user

    @classmethod
    def authorize_by_token(cls, token):
        # create your own method of authorize with token
        res = sql_req(...)
        if not res or not verify_hashed_string(...):
            raise InvalidTokenError
        user = cls.get(res.get('id'))
        return user

    @classmethod  # create unverified user, by my logic, he must to click on url in his email message
    def create(cls, **kwargs):
        sql_insert('unverified_users', **kwargs)

    # BAD IDEA HOW TO SEND NOTIFICATION TO USER PHONE, BUT WORKING
    # @staticmethod
    # def send_notify(body, header, to_id, extras=None):
    #     user = User.get(to_id)
    #     res_ = sql_req('SELECT token FROM `mobile_tokens` WHERE email=%s', user.email, fetch_one=True)
    #     adnr = messaging.AndroidConfig(
    #         ttl=datetime.timedelta(seconds=3600),
    #         priority='high',
    #         notification=messaging.AndroidNotification(
    #             icon='resize_300x0',
    #             visibility='public'
    #         ),
    #     )
    #     data = {}
    #     if extras is not None:
    #         for i in extras.split('&'):
    #             data.update({i.split('=')[0]: i.split('=')[1]})
    #         message = messaging.Message(
    #             notification=messaging.Notification(
    #                 title=header,
    #                 body=body,
    #             ),
    #             android=adnr,
    #             apns=messaging.APNSConfig(
    #                 payload=messaging.APNSPayload(
    #                     aps=messaging.Aps(badge=42),
    #                 ),
    #             ),
    #             data=data,
    #             token=res_.get('token')
    #         )
    #     else:
    #         message = messaging.Message(
    #             notification=messaging.Notification(
    #                 title=header,
    #                 body=body,
    #             ),
    #             android=adnr,
    #             apns=messaging.APNSConfig(
    #                 payload=messaging.APNSPayload(
    #                     aps=messaging.Aps(badge=42),
    #                 ),
    #             ),
    #             token=res_.get('token')
    #         )
    #     try:
    #         messaging.send(message)
    #     except Exception as e:
    #         pass

    @property
    def to_dict(self):
        return {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.full_name,
            'id': self.id,
        }

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def update(self,
               **kwargs):  # method for update user fields in you MySQL db like update(first_name="new first name")
        updates = ','.join([f'{k}=%s' for k in kwargs])
        sql_req(f'UPDATE `users` SET {updates} WHERE id=%s', *kwargs.values(), self.id)
        vars(self).update(kwargs)
