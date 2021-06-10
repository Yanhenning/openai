from cerberus import Validator

from api.datastore_gateway.datastore_gateway import DatastoreGateway


def get_user_by_username(username):
    schema = {'username': {'type': 'string', 'coerce': str}}
    validator = Validator(schema)
    validator.validate({'username': username})

    datastore_gateway = DatastoreGateway('user')
    return datastore_gateway.get_one(username=('=', validator.document['username']))
