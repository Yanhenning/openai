import os
from flask import Flask
from google.cloud import datastore

from api.datastore_gateway.datastore_gateway import DatastoreGateway

app = Flask(__name__)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"


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
    return f'Usuario retornado {username}'


@app.post('/user')
def create_user():
    return 'Usuario criado'


@app.put('/user/<string:username>')
def edit_user(username):
    return f'Usuario {username} alterado'


if __name__ == "__main__":
    app.run()
