from api.datastore_gateway.datastore_gateway import DatastoreGateway


def get_accounts():
    datastore_gateway = DatastoreGateway('account')
    return datastore_gateway.get()
