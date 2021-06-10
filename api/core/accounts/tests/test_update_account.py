from unittest import TestCase
from unittest.mock import patch

from api.core.accounts.update_account import update_account
from api.core.exceptions import EntityDoesNotExist


class UpdateAccountTests(TestCase):

    @patch('api.core.accounts.update_account.DatastoreGateway.__init__')
    @patch('api.core.accounts.update_account.DatastoreGateway.get_by_id')
    @patch('api.core.accounts.update_account.DatastoreGateway.update')
    def test_update_account(self, update_mock, get_by_id_mock, init_mock):
        init_mock.return_value = None
        account_id = 1
        get_by_id_mock.return_value = {'id': account_id, 'fullName': 'Zé silva'}
        new_data = {'fullName': 'Zé da silva'}

        update_account(account_id, new_data)

        update_mock.assert_called_with(account_id, **new_data)

    @patch('api.core.accounts.update_account.DatastoreGateway.__init__')
    @patch('api.core.accounts.update_account.DatastoreGateway.get_by_id')
    def test_throw_exception_when_account_does_not_exist(self, get_by_id_mock, init_mock):
        init_mock.return_value = None
        account_id = 1
        get_by_id_mock.return_value = None
        new_data = {'fullName': 'Zé da silva'}

        with self.assertRaises(EntityDoesNotExist) as context:
            update_account(account_id, new_data)

        expected_error = {'account': [f'Account (id: {account_id}) does not exist']}
        self.assertEqual(expected_error, context.exception.errors)
