from datetime import date, timedelta
from unittest import TestCase

from api.core.exceptions import ValidationError
from api.core.validators import validate_account, DATE_FORMAT


class ValidateAccountTests(TestCase):
    def test_all_fields_are_required_when_is_insertion(self):
        with self.assertRaises(ValidationError) as context:
            validate_account({}, is_insertion=True)

        self.assertIn('document', context.exception.errors)
        self.assertIn('fullName', context.exception.errors)
        self.assertIn('email', context.exception.errors)
        self.assertIn('phone', context.exception.errors)
        self.assertIn('birthDate', context.exception.errors)

    def test_all_fields_are_optional_when_is_not_insertion(self):
        validate_account({}, is_insertion=False)


class ValidateCpfTests(TestCase):
    def test_validate_document_with_punctuation(self):
        validated_data = validate_account({'document': '512.027.250-90'}, is_insertion=False)

        self.assertEqual('51202725090', validated_data['document'])

    def test_validate_document_without_punctuation(self):
        validated_data = validate_account({'document': '51202725090'}, is_insertion=False)

        self.assertEqual('51202725090', validated_data['document'])

    def test_exception_when_document_is_invalid(self):
        with self.assertRaises(ValidationError) as context:
            validate_account({'document': '515090'}, is_insertion=False)

        self.assertIn('document', context.exception.errors)


class ValidateEmailTests(TestCase):
    def test_validate_email(self):
        validated_data = validate_account({'email': 'yan@gmail.com'}, is_insertion=False)

        self.assertEqual('yan@gmail.com', validated_data['email'])

    def test_exception_when_email_is_invalid(self):
        with self.assertRaises(ValidationError) as context:
            validate_account({'email': 'yangmail.com'}, is_insertion=False)

        self.assertIn('email', context.exception.errors)

    def test_exception_when_dot_com_is_missing(self):
        with self.assertRaises(ValidationError) as context:
            validate_account({'email': 'yan@gmail'}, is_insertion=False)

        self.assertIn('email', context.exception.errors)

    def test_exception_when_email_is_empty(self):
        with self.assertRaises(ValidationError) as context:
            validate_account({'email': ''}, is_insertion=False)

        self.assertIn('email', context.exception.errors)


class ValidateBirthdateTests(TestCase):
    def test_validate_birthdate(self):
        eighteen_years_ago = date.today() + timedelta(days=366 * 18)
        birthdate = eighteen_years_ago.strftime(DATE_FORMAT)

        validated_data = validate_account({'birthDate': birthdate}, is_insertion=False)

        self.assertEqual(birthdate, validated_data['birthDate'])

    def test_exception_when_age_is_under_18(self):
        with self.assertRaises(ValidationError) as context:
            validate_account({'birthDate': date.today().strftime(DATE_FORMAT)}, is_insertion=False)

        self.assertIn('birthDate', context.exception.errors)
        self.assertIn('Age must be over 18 years old', context.exception.errors['birthDate'][0])


class ValidatePhoneTests(TestCase):
    def test_validate_phone(self):
        phone = '(47) 98844-4444'

        validated_data = validate_account({'phone': phone}, is_insertion=False)

        self.assertEqual(phone, validated_data['phone'])

    def test_validate_phone_without_punctuation(self):
        phone = '47988444444'

        validated_data = validate_account({'phone': phone}, is_insertion=False)

        self.assertEqual(phone, validated_data['phone'])

    def test_exception_when_age_is_under_18(self):
        with self.assertRaises(ValidationError) as context:
            validate_account({'phone': ''}, is_insertion=False)

        self.assertIn('phone', context.exception.errors)
