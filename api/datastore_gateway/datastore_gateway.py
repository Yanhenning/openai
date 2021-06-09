from google.cloud import datastore


class DatastoreGateway:
    def __init__(self, entity_type, namespace='usuario'):
        self.namespace = namespace
        self.entity_type = entity_type
        self.client = datastore.Client()

    def get_all(self):
        pass

    def get(self, **filters):
        pass

    def create(self, **data):
        with self.client.transaction():
            entity_key = self.client.key(self.entity_type, namespace=self.namespace)
            entity = datastore.Entity(key=entity_key)
            entity.update(**data)
            self.client.put(entity)

    def update(self, username, email, **data):
        pass

    def upset(self, username, email, **data):
        pass

    def delete(self, username, email):
        pass
