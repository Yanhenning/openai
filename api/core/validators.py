import re
from datetime import datetime, date

from cerberus import Validator

from api.core.exceptions import ValidationError


def divisor(v):
    if v >= 2:
        return 11 - v
    return 0


def validate_id(field, value, error):
    try:
        value = int(value)
    except ValueError:
        error(field, 'Cannot convert the value to integer')

    if value <= 0:
        error(field, 'Id must be greater than 0')


def validator_entity_id(entity_id):
    schema = {'id': {'type': 'integer', 'check_with': validate_document, 'coerce': int}}
    validator = Validator(schema, purge_unknown=True)
    validator.validate({'id': entity_id})

    if validator.errors:
        if validator.errors:
            raise ValidationError(validator.errors)

    return validator.document['id']


def validate_document(field, value, error):
    try:
        if not value.isdigit():
            value = strip_points(value)
        try:
            int(value)
        except ValueError:
            error(field, 'Cannot convert the value to integer')
        if len(value) != 11:
            error(field, 'The CPF must have 11 digits')
        original_division = value[-2:]

        first_division = sum([i * int(value[idx]) for idx, i in enumerate(range(10, 1, -1))])
        first_division = divisor(first_division % 11)
        value = value[:-2] + str(first_division) + value[-1]
        second_division = sum([i * int(value[idx]) for idx, i in enumerate(range(11, 1, -1))])
        second_division = divisor(second_division % 11)
        value = value[:-1] + str(second_division)
        if value[-2:] != original_division:
            error(field, 'CPF invalid')

        if len(set(value)) == 1:
            error(field, 'CPF invalid')

    except IndexError:
        error(field, 'CPF invalid')


email_pattern = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')


def validate_email(field, value, error):
    if not email_pattern.match(value):
        error(field, f'Invalid e-mail pattern e-mail received: {value}')


phone_pattern = re.compile(
    r'^1\d\d(\d\d)?$|^0800 ?\d{3} ?\d{4}$|^(\(0?([1-9a-zA-Z][0-9a-zA-Z])?[1-9]\d\) ?|0?([1-9a-zA-Z][0-9a-zA-Z])?[1-9]\d[ .-]?)?(9|9[ .-])?[2-9]\d{3}[ .-]?\d{4}$'
)


def validate_phone(field, value, error):
    if not phone_pattern.match(value):
        error(field, f'Invalid phone format phone received: {value}')


DATE_FORMAT = '%d/%m/%Y'
HEURISTIC_CONSTANT = 365.25


def validate_birthdate(field, value, error):
    if not value:
        return

    birthdate = None
    if isinstance(value, datetime) or isinstance(value, date):
        birthdate = value
    try:
        birthdate = datetime.strptime(value, DATE_FORMAT).date()
    except ValueError:
        error(field, f'Invalid format for date format allowed {DATE_FORMAT}')

    age = abs((date.today() - birthdate).days / HEURISTIC_CONSTANT)

    if age < 18:
        error(field, 'Age must be over 18 years old')


def strip_points(value):
    return re.sub('[-\.\s]', '', value)


def get_account_schema(is_insertion=True):
    return {
        "document": {"type": "string", "required": is_insertion, 'check_with': validate_document, 'coerce': strip_points},
        "username": {"type": "string", "required": False, 'empty': False},
        "fullName": {"type": "string", "required": is_insertion, 'empty': False},
        "email": {"type": "string", "required": is_insertion, 'check_with': validate_email, 'empty': False},
        "phone": {"type": "string", "required": is_insertion, 'check_with': validate_phone},
        "birthDate": {"type": "string", "required": is_insertion, 'check_with': validate_birthdate},
    }


def validate_account(data, is_insertion=True):
    account_schema = get_account_schema(is_insertion)
    validator = Validator(account_schema, purge_unknown=True)
    validator.validate(data)

    if validator.errors:
        raise ValidationError(validator.errors)

    return validator.document


def validate_account_creation(data):
    return validate_account(data, is_insertion=True)


def validate_account_uptade(data):
    return validate_account(data, is_insertion=False)
