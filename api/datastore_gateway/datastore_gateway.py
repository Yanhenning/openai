from datetime import datetime

from google.cloud import datastore


class DefaultFieldsEnum:
    UPDATED_AT = 'updated_at'
    CREATED_AT = 'created_at'
    EXCLUDED = 'excluded'


class DatastoreGateway:
    def __init__(self, entity_type, namespace='usuario'):
        self.namespace = namespace
        self.entity_type = entity_type
        self.client = datastore.Client()

    def mount_complete_key(self, **filters: dict):
        args = []

        for key, value in filters.items():
            args.append(key)
            args.append(value)

        return self.client.key(*tuple(args))

    def get_all(self):
        pass

    def get(self, **filters: dict):
        key = self.mount_complete_key(**filters)
        return self.client.get(key)

    def create(self, **data):
        with self.client.transaction():
            entity_key = self.client.key(self.entity_type, namespace=self.namespace)
            entity = datastore.Entity(key=entity_key)

            datetime_now = datetime.now()
            entity_data = {
                DefaultFieldsEnum.CREATED_AT: datetime_now,
                DefaultFieldsEnum.UPDATED_AT: datetime_now,
                DefaultFieldsEnum.EXCLUDED: False,
                **data
            }

            entity.update(entity_data)
            self.client.put(entity)

    def update(self, filters: dict, **data):
        with self.client.transaction():
            key = self.mount_complete_key(**filters)
            entity = datastore.Entity(key=key)

            for key, value in data.items():
                entity[key] = value
            entity[DefaultFieldsEnum.UPDATED_AT] = datetime.now()

            self.client.put(entity)

    def delete(self, **filters):
        self.update(filters, excluded=True)
