"""
this file to work with mail server like send message and etc.
"""

from flask_mail import Mail, Message
from pyisemail import is_email
from pyisemail.validators.dns_validator import dns

from api.api_exceptions import BadEmail

mail = Mail()


def send_email(target, topic, message):
    try:
        if not is_email(target, True):
            raise BadEmail(target)
    except dns.resolver.NoNameservers:
        raise BadEmail(target)
    msg = Message(topic,
                  sender=('sender', "your_email@mail.ru"),
                  recipients=[target], body=message)
    mail.send(msg)


def verification_email(target, vercode):
    send_email(target, topic="Email verification",
               message=f'Verification code: https://you_url.com/verification?code={vercode}')


def reset_password(target, code):
    send_email(target, topic="Reset password",
               message=f'Message to reset code: http://you_url.com/reset_password?code={code}')


def send_message(email, topic, message):
    send_email(email, topic, message)
