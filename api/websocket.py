from flask import request
from flask_socketio import SocketIO, send, ConnectionRefusedError

from api import sosite_json
from api.api_exceptions import InvalidTokenError
from api.constants import APP_NAME
from api.objects import User

socketio = SocketIO(path=f'/{APP_NAME}/websocket', json=sosite_json, cors_allowed_origins='*', async_mode='gevent')

socketio.clients = {}


def validate_token():
    auth = request.headers.get('Authorization')
    if not auth or ' ' not in auth:
        raise ConnectionRefusedError('Unauthorized.')
    token = auth.split(' ', 1)[1]
    try:
        user = User.authorize_by_token(token)
    except InvalidTokenError:
        raise ConnectionRefusedError('Unauthorized.')
    return user


@socketio.event
def connect():
    user = validate_token()
    if user.id not in socketio.clients:
        socketio.clients[user.id] = []
    socketio.clients[user.id].append(request.sid)
    # join_room(f'user_id{user.id}')
    send({'status': 'connected', 'response': user})


@socketio.event
def disconnect():
    for user in socketio.clients:
        if request.sid in socketio.clients[user]:
            socketio.clients[user].remove(request.sid)


# an example of calling the event of sending a message to a chat for users
def send_message_to_chat(chat_id, message):
    socketio.emit('new_message', message, room=f'chat{chat_id}')
