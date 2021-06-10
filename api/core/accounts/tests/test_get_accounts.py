from unittest import TestCase
from unittest.mock import patch

from api.core.accounts.get_accounts import get_accounts


class GetAccountsTests(TestCase):

    @patch('api.core.accounts.get_accounts.DatastoreGateway.__init__')
    @patch('api.core.accounts.get_accounts.DatastoreGateway.get')
    def test_return_accounts(self, get_mock, init_mock):
        init_mock.return_value = None
        get_mock.return_value = [{'id': 1}]

        result = get_accounts()

        self.assertEqual(1, len(result))
        self.assertEqual({'id': 1}, result[0])
