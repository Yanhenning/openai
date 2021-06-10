import logging
import os
from flask import Flask, jsonify
from flask import request

from api.core.exceptions import ValidationError
from api.core.user.create_user import insert_user
from api.datastore_gateway.datastore_gateway import DatastoreGateway

app = Flask(__name__)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "apiconfig.json"


@app.route('/')
def hello_world():
    return 'Hello, World!3'


@app.route('/teste')
def hello_world2():
    client_usuario = DatastoreGateway('usuario')
    entities = client_usuario.create(**{'username': 'Yan'})
    return 'criado'


@app.get('/user/<string:username>')
def get_user(username):
    client_usuario = DatastoreGateway('usuario')
    return client_usuario.get(username=('=', username))


@app.post('/user')
def create_user():
    try:
        created_user = insert_user(request.json)
    except ValidationError as context:
        return jsonify(context.errors), 400
    return created_user


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return """
    An internal error occurred: <pre>{}</pre>
    See logs for full stacktrace.
    """.format(e), 500


@app.put('/user/<string:username>')
def edit_user(username):
    return f'Usuario {username} alterado'


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)
