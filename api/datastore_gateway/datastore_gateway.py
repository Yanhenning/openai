from datetime import datetime

from google.cloud import datastore


class DefaultFieldsEnum:
    UPDATED_AT = 'updated_at'
    CREATED_AT = 'created_at'
    EXCLUDED = 'excluded'


class DatastoreGateway:
    def __init__(self, entity_type, namespace='development'):
        self.namespace = namespace
        self.entity_type = entity_type
        self.client = datastore.Client()

    def get(self, **filters):
        query = self.client.query(kind=self.entity_type, namespace=self.namespace)
        query_filters = [(key, value[0], value[1]) for key, value in filters.items()]
        for query_filter in query_filters:
            query.add_filter(*query_filter)

        return list(query.fetch())

    def get_one(self, **filters):
        results = self.get(**filters)
        if results:
            return results[0]
        return

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

    def update(self, key, **data):
        with self.client.transaction():
            entity = datastore.Entity(key=key)

            for key, value in data.items():
                entity[key] = value
            entity[DefaultFieldsEnum.UPDATED_AT] = datetime.now()

            self.client.put(entity)

    def delete(self, **filters):
        self.update(filters, excluded=True)
