from api.core.exceptions import EntityDoesNotExist
from api.core.validators import validate_account_uptade, validator_entity_id
from api.datastore_gateway.datastore_gateway import DatastoreGateway


def update_account(account_id, data):
    account_id = validator_entity_id(account_id)
    validated_data = validate_account_uptade(data)
    datastore_gateway = DatastoreGateway('account')

    account = datastore_gateway.get_by_id(account_id)
    if not account:
        raise EntityDoesNotExist(errors={'account': [f'Account (id: {account_id}) does not exist']})

    datastore_gateway.update(account_id, **validated_data)
    return account_id
