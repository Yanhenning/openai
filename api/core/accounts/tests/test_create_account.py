from unittest import TestCase
from unittest.mock import patch, call

from api.core.accounts.create_account import create_account
from api.core.exceptions import ValidationError


class CreateAccountTests(TestCase):

    @patch('api.core.accounts.create_account.DatastoreGateway.get_one')
    @patch('api.core.accounts.create_account.DatastoreGateway.create')
    def test_create_account(self, create_mock, get_one_mock):
        data = {
            "document": "15380060064",
            "fullName": "Jurandir",
            "email": "jurandir@gmail.com",
            "phone": "4798838888",
            "birthDate": "22/03/2001"
        }
        create_mock.return_value = 1
        get_one_mock.return_value = None

        result = create_account(data)

        create_mock.assert_called_with(**data)
        get_one_mock.assert_has_calls([
            call(document=('=', data['document']), excluded=('=', False)),
            call(email=('=', data['email']), excluded=('=', False))
        ])
        self.assertEqual(1, result['id'])

    @patch('api.core.accounts.create_account.DatastoreGateway.get_one')
    @patch('api.core.accounts.create_account.DatastoreGateway.create')
    def test_dont_create_an_account_when_already_exists_a_account_with_given_document(self, create_mock, get_one_mock):
        data = {
            "document": "15380060064",
            "fullName": "Jurandir",
            "email": "jurandir@gmail.com",
            "phone": "4798838888",
            "birthDate": "22/03/2001"
        }
        create_mock.return_value = 1
        account_registered = {
            'document': data['document'],
            'email': 'email@email.com'
        }
        get_one_mock.side_effect = [account_registered, None]

        with self.assertRaises(ValidationError) as context:
            create_account(data)

        create_mock.assert_not_called()
        self.assertIn('document', context.exception.errors)
        self.assertIn('Document already registered', context.exception.errors['document'])

    @patch('api.core.accounts.create_account.DatastoreGateway.get_one')
    @patch('api.core.accounts.create_account.DatastoreGateway.create')
    def test_dont_create_an_account_when_already_exists_a_account_with_given_email(self, create_mock, get_one_mock):
        data = {
            "document": "15380060064",
            "fullName": "Jurandir",
            "email": "jurandir@gmail.com",
            "phone": "4798838888",
            "birthDate": "22/03/2001"
        }
        create_mock.return_value = 1
        account_registered = {
            'document': '26048118040',
            'email': data['email']
        }
        get_one_mock.side_effect = [None, account_registered]

        with self.assertRaises(ValidationError) as context:
            create_account(data)

        create_mock.assert_not_called()
        self.assertIn('email', context.exception.errors)
        self.assertIn('E-mail already registered', context.exception.errors['email'])

    def test_throw_exception_when_data_is_invaliad(self):
        with self.assertRaises(ValidationError) as context:
            create_account({})

        self.assertIn('document', context.exception.errors)
        self.assertIn('birthDate', context.exception.errors)
        self.assertIn('email', context.exception.errors)
        self.assertIn('fullName', context.exception.errors)
        self.assertIn('phone', context.exception.errors)
