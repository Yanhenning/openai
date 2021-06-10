from api.core.exceptions import ValidationError
from api.core.validators import validate_account_creation
from api.datastore_gateway.datastore_gateway import DatastoreGateway


def insert_account(data):
    validated_account = validate_account_creation(data)
    datastore_gateway = DatastoreGateway('account')

    account_document = datastore_gateway.get_one(document=('=', validated_account['document']), excluded=('=', False))
    account_email = datastore_gateway.get_one(email=('=', validated_account['email']), excluded=('=', False))
    errors = {}
    if account_document:
        errors['document'] = ['Document already registered']
    if account_email:
        errors['email'] = ['E-mail is already used']
    if errors:
        raise ValidationError(errors)

    account_id = datastore_gateway.create(**validated_account)
    validated_account['id'] = account_id
    return validated_account
