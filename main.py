import logging
import os
from flask import Flask, jsonify
from flask import request

from api.core.exceptions import ValidationError
from api.core.user.get_user_by_username import get_user_by_username
from api.core.user.insert_user import insert_user
from api.datastore_gateway.datastore_gateway import DatastoreGateway

app = Flask(__name__)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "apiconfig.json"


@app.route('/')
def hello_world():
    return 'Hello, World!3'


@app.get('/user/<string:username>')
def get_user(username):
    user = get_user_by_username(username)
    if not user:
        return {'username': f'User with {username} username does not exist'}, 404
    return user, 200


@app.post('/user')
def create_user():
    try:
        created_user = insert_user(request.json)
    except ValidationError as context:
        return jsonify(context.errors), 400
    return created_user, 200


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return f"""
    An internal error occurred: <pre>{e}</pre>
    See logs for full stacktrace.
    """, 500


@app.put('/user/<string:username>')
def edit_user(username):
    return f'Usuario {username} alterado'


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)
