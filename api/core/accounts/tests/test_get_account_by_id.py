from unittest import TestCase
from unittest.mock import patch

from api.core.accounts.get_account_by_id import get_account_by_id


class GetAccountByIdTests(TestCase):
    @patch('api.core.accounts.get_account_by_id.DatastoreGateway.get_by_id')
    def test_return_accounts(self, get_by_id_mock):
        account_id = 1
        get_by_id_mock.return_value = {'id': account_id}

        result = get_account_by_id(account_id=account_id)

        self.assertEqual({'id': account_id}, result)
        get_by_id_mock.assert_called_with(account_id)

    @patch('api.core.accounts.get_account_by_id.DatastoreGateway.get_by_id')
    def test_validate_id(self, get_by_id_mock):
        account_id = 1
        get_by_id_mock.return_value = {'id': account_id}

        result = get_account_by_id(account_id=str(account_id))

        self.assertEqual({'id': account_id}, result)
