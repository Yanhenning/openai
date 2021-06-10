from api.core.validators import validator_entity_id
from api.datastore_gateway.datastore_gateway import DatastoreGateway


def get_account_by_id(account_id):
    account_id = validator_entity_id(account_id)
    datastore_gateway = DatastoreGateway('account')
    return datastore_gateway.get_by_id(account_id)
