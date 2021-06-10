import logging
import os
from flask import Flask, jsonify
from flask import request

from api.core.exceptions import ValidationError
from api.core.request_decorators import error_handler
from api.core.user.get_user_by_username import get_user_by_username
from api.core.user.insert_user import insert_user
from api.core.user.update_user import update_user

app = Flask(__name__)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "apiconfig.json"


@app.route('/')
def hello_world():
    return 'Hello, World!3'


@app.get('/user/<string:username>')
@error_handler
def get_user(username):
    user = get_user_by_username(username)
    return user, 200


@app.post('/user')
@error_handler
def create_user():
    created_user = insert_user(request.json)
    return created_user, 200


@app.post('/user/createWithList')
@error_handler
def create_user_with_list():
    return 'users created'


@app.put('/user/<string:username>')
@error_handler
def edit_user(username):
    username = update_user(username, request.json or {})
    return {'username': username}, 200


@app.delete('/user/<string:username>')
@error_handler
def delete_user(username):
    return f'${username} deleted'


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return f"""
    An internal error occurred: <pre>{e}</pre>
    See logs for full stacktrace.
    """, 500


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)
