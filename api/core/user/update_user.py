from api.core.exceptions import EntityDoesNotExist
from api.core.validators import validate_user_uptade
from api.datastore_gateway.datastore_gateway import DatastoreGateway


def update_user(username, data):
    data['username'] = username
    validated_data = validate_user_uptade(data)

    datastore_gateway = DatastoreGateway('user')
    user = datastore_gateway.get_one(username=('=', validated_data['username']))

    if not user:
        raise EntityDoesNotExist(errors={'user': [f'User ({username}) does not exist']})

    datastore_gateway.update(user['key'], **validated_data)

    return username
