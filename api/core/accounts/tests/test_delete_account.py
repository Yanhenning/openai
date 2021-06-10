from unittest import TestCase
from unittest.mock import patch

from api.core.accounts.delete_account import delete_account


class DeleteAccountTests(TestCase):

    @patch('api.core.accounts.delete_account.DatastoreGateway.delete')
    def test_delete_account(self, delete_mock):
        account_id = 1

        delete_account(account_id)

        delete_mock.assert_called_with(account_id)
