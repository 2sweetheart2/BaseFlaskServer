from firebase_admin import initialize_app, credentials
from flask import Flask, redirect
from flask_login import LoginManager

from api.api_exceptions import *
from api.api_main import my_blueprint
from api.objects import User
from api.websocket import socketio

app = Flask(__name__, static_url_path='')

app.register_blueprint(my_blueprint)  # you can register you blueprint

# IF YOU NEED LOGIN/REGISTER OF WEBSITE, YOU CAN USE LoginManager from flask_login
login_manager = LoginManager()
login_manager.login_view = 'you_endpoint.login'  # set the end-point for login
login_manager.init_app(app)


@login_manager.user_loader  # when the user has already been logged in and visits the page again
def load_user(user_id):
    try:
        return User.get(user_id)
    except UserNotFound:
        redirect("your.url.redirect.when.cant.relogin")


# this information is needed to connect the mail ->
# app.config.update({
#     'DEBUG': False,
#     'MAIL_SERVER': 'your.mail.server',
#     'MAIL_PORT': your_mail_port,
#     'MAIL_USE_TLS': False,
#     'MAIL_USE_SSL': True,
#     'MAIL_USERNAME': 'your_mail@mail.ru,
#     'MAIL_PASSWORD': 'your mail password',
# })
# mail.init_app(app)

# THIS BLOCK OF INFO NEEDED TO USE GOOGLE FIREBASE
app.config['SECRET_KEY'] = 'your_firebase_secret_key'
cred = credentials.Certificate(str(FBS_PATH / 'fbs-token.json'))
initialize_app(cred)

socketio.init_app(app)

if __name__ == '__main__':
    # if you want to run the server locally ->
    # app.run()

    # if you don't need a socket, to run the server globally ->
    # server = WSGIServer(bind_addr=('0.0.0.0', 8200), wsgi_app=app, numthreads=1)
    # try:
    #     server.start()
    # except KeyboardInterrupt:
    #     server.stop()
    # except Exception as e:
    #     print(e)

    # if you are using socket ->
    socketio.run(app, '0.0.0.0', 8200)
