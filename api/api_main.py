from flask import jsonify, request, Blueprint

from api.constants import *
from api.methods import *

my_blueprint = Blueprint(APP_NAME, __name__, template_folder='templates')
"""
I prefer to store post methods this way, but if desired, you can create several dicts for different types of requests.

If you have to use several types of requests [post, get, delete, etc.],
I recommend making the same function that will accept only one type of request
"""
methods = {
    'my_method': MyMethod
}


# get_methods = { 'my_get_method' : MyGetMethod }
# post_methods = { 'my_post_method': MyPostMethod }

@my_blueprint.route('/api/<method>', methods=['POST'])
def send_methods(method):
    kwargs = dict(request.values)  # parse all info (url parameters, json,files) in one dict
    if request.is_json:
        kwargs.update(request.json)
    if request.files:
        kwargs.update(request.files)
    try:
        res = api_request(method=method, **kwargs)
    except InvalidRequest as e:
        return jsonify(success=False, error={'code': e.code, 'string': e.string, 'message': e.message})
    return jsonify(success=True, response=res)


def find_method(method):  # find requested method in our dict
    if method in methods:
        return methods.get(method)
    raise InvalidMethod


def api_request(**kwargs):
    method = kwargs.pop('method', None)
    return find_method(method)().process(**kwargs)  # calling our found method with parameters


"""
if you wont add websocket methods, do this ->
"""
# for _method in websocket_methods:
#     from api.websocket import socketio
#
#     socketio.on_event(_method, websocket_api_callback(_method))
