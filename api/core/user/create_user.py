from api.core.validators import validate_user_creation
from api.datastore_gateway.datastore_gateway import DatastoreGateway


def insert_user(data):
    validated_user = validate_user_creation(data)
    datastore_gateway = DatastoreGateway('user')
    datastore_gateway.create(**validated_user)

    return validated_user
