from api.core.validators import validator_entity_id
from api.datastore_gateway.datastore_gateway import DatastoreGateway


def delete_account(account_id):
    account_id = validator_entity_id(account_id)
    DatastoreGateway('account').delete(account_id)
    return account_id
