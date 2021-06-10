from datetime import datetime
from unittest import TestCase
from unittest.mock import patch, call

from api.datastore_gateway.datastore_gateway import DatastoreGateway, DefaultFieldsEnum


class DatastoreGatewayTests(TestCase):
    @patch('api.datastore_gateway.datastore_gateway.datastore')
    def test_create_client(self, datastore_mock):
        DatastoreGateway(entity_type='usuario')

        datastore_mock.Client.assert_called()

    @patch('api.datastore_gateway.datastore_gateway.datastore')
    def test_create_gateway_with_entity_type(self, datastore_mock):
        datastore_gateway = DatastoreGateway(entity_type='usuario')

        self.assertEqual('usuario', datastore_gateway.entity_type)

    @patch('api.datastore_gateway.datastore_gateway.datastore')
    def test_create_gateway_with_given_namespace(self, datastore_mock):
        datastore_gateway = DatastoreGateway(entity_type='usuario', namespace='development')

        self.assertEqual('development', datastore_gateway.namespace)

    @patch('api.datastore_gateway.datastore_gateway.datastore')
    def test_base_query_with_gateway_attributes(self, datastore_mock):
        datastore_gateway = DatastoreGateway(entity_type='usuario', namespace='development')

        datastore_gateway.get()

        datastore_mock.Client().query.assert_called_with(kind='usuario', namespace='development')

    @patch('api.datastore_gateway.datastore_gateway.datastore')
    def test_add_filters_to_base_query_passing_as_named_param(self, datastore_mock):
        datastore_gateway = DatastoreGateway(entity_type='usuario', namespace='development')

        datastore_gateway.get(username=('=', 'yanhenning'))

        datastore_mock.Client().query().add_filter.assert_called_with('username', '=', 'yanhenning')

    @patch('api.datastore_gateway.datastore_gateway.datastore')
    def test_add_filters_to_base_query_passing_as_dict(self, datastore_mock):
        datastore_gateway = DatastoreGateway(entity_type='usuario', namespace='development')

        datastore_gateway.get(**{'username': ('=', 'yanhenning')})

        datastore_mock.Client().query().add_filter.assert_called_with('username', '=', 'yanhenning')

    @patch('api.datastore_gateway.datastore_gateway.datastore')
    def test_add_multiple_filters(self, datastore_mock):
        datastore_gateway = DatastoreGateway(entity_type='usuario', namespace='development')

        datastore_gateway.get(username=('=', 'yanhenning'), lastname=('=', 'henning'))

        datastore_mock.Client().query().add_filter.assert_has_calls(
            [
                call('username', '=', 'yanhenning'),
                call('lastname', '=', 'henning')
            ]
        )

    @patch('api.datastore_gateway.datastore_gateway.datastore')
    def test_return_values_from_datastore(self, datastore_mock):
        datastore_gateway = DatastoreGateway(entity_type='usuario')
        datastore_mock.Client().query().fetch.return_value = [1, 2]

        entities = datastore_gateway.get()

        self.assertEqual(2, len(entities))

    @patch('api.datastore_gateway.datastore_gateway.datastore')
    def test_return_one_value_when_register_exists(self, datastore_mock):
        datastore_gateway = DatastoreGateway(entity_type='usuario')
        datastore_mock.Client().query().fetch.return_value = [1]

        entity = datastore_gateway.get_one()

        self.assertEqual(1, entity)

    @patch('api.datastore_gateway.datastore_gateway.datastore')
    def test_return_none_when_register_not_exists(self, datastore_mock):
        datastore_gateway = DatastoreGateway(entity_type='usuario')
        datastore_mock.Client().query().fetch.return_value = []

        self.assertIsNone(datastore_gateway.get_one())

    @patch('api.datastore_gateway.datastore_gateway.datastore')
    def test_get_by_entity_id(self, datastore_mock):
        datastore_gateway = DatastoreGateway(entity_type='usuario')
        datastore_mock.Client.key.return_value = {'id': 1}

        entity = datastore_gateway.get_by_id(entity_id=1)

        datastore_mock.Client().key.called_with(datastore_gateway.entity_type, 1, namespace=datastore_gateway.namespace)
        datastore_mock.Client().get.called_with({'id': 1})

    @patch('api.datastore_gateway.datastore_gateway.datastore')
    def test_return_entity_by_id(self, datastore_mock):
        datastore_gateway = DatastoreGateway(entity_type='usuario')
        datastore_mock.Client().get.return_value = {'id': 1}

        entity = datastore_gateway.get_by_id(entity_id=1)

        self.assertEqual({'id': 1}, entity)


class DatastoreGatewayCreateTests(TestCase):
    @patch('api.datastore_gateway.datastore_gateway.datastore')
    def test_create_a_key_with_entity_type(self, datastore_mock):
        datastore_gateway = DatastoreGateway(entity_type='usuario')

        datastore_gateway.create()

        datastore_mock.Client().key.assert_called_with(datastore_gateway.entity_type, namespace=datastore_gateway.namespace)

    @patch('api.datastore_gateway.datastore_gateway.datastore')
    def test_send_entity_to_datastore(self, datastore_mock):
        datastore_gateway = DatastoreGateway(entity_type='usuario')

        datastore_gateway.create()

        datastore_mock.Client().put.assert_called_once()

    @patch('api.datastore_gateway.datastore_gateway.datetime')
    @patch('api.datastore_gateway.datastore_gateway.datastore')
    def test_create_entity_with_default_attributes(self, datastore_mock, datetime_mock):
        datastore_gateway = DatastoreGateway(entity_type='usuario')
        now = datetime(2020, 1, 1, 0, 0, 0)
        datetime_mock.now.return_value = now

        datastore_gateway.create()

        datastore_mock.Entity().update.assert_called_with(
            {
                DefaultFieldsEnum.CREATED_AT: now,
                DefaultFieldsEnum.UPDATED_AT: now,
                DefaultFieldsEnum.EXCLUDED: False,
            }
        )

    @patch('api.datastore_gateway.datastore_gateway.datetime')
    @patch('api.datastore_gateway.datastore_gateway.datastore')
    def test_create_entity_with_data_passed(self, datastore_mock, datetime_mock):
        datastore_gateway = DatastoreGateway(entity_type='usuario')
        now = datetime(2020, 1, 1, 0, 0, 0)
        datetime_mock.now.return_value = now

        datastore_gateway.create(username='yanhenning')

        datastore_mock.Entity().update.assert_called_with(
            {
                DefaultFieldsEnum.CREATED_AT: now,
                DefaultFieldsEnum.UPDATED_AT: now,
                DefaultFieldsEnum.EXCLUDED: False,
                'username': 'yanhenning'
            }
        )


class DatastoreGatewayUpdateTests(TestCase):
    @patch('api.datastore_gateway.datastore_gateway.datastore')
    def test_get_entity_by_id(self, datastore_mock):
        datastore_gateway = DatastoreGateway(entity_type='usuario')

        datastore_gateway.update(entity_id=1)

        datastore_mock.Client().key.assert_called_with(datastore_gateway.entity_type, 1, namespace=datastore_gateway.namespace)

    @patch('api.datastore_gateway.datastore_gateway.datastore')
    def test_send_entity_to_datastore(self, datastore_mock):
        datastore_gateway = DatastoreGateway(entity_type='usuario')

        datastore_gateway.update('key')

        datastore_mock.Client().put.assert_called_once()
