from api.core.exceptions import ValidationError
from api.core.validators import validate_user_creation
from api.datastore_gateway.datastore_gateway import DatastoreGateway


def insert_user(data):
    validated_user = validate_user_creation(data)
    datastore_gateway = DatastoreGateway('user')

    user_cpf = datastore_gateway.get_one(username=('=', validated_user['username']))
    user_email = datastore_gateway.get_one(email=('=', validated_user['email']))
    errors = {}
    if user_cpf:
        errors['cpf'] = ['CPF is already registered']
    if user_email:
        errors['email'] = ['E-mail is already used']
    if errors:
        raise ValidationError(errors)

    datastore_gateway.create(**validated_user)
    return validated_user
