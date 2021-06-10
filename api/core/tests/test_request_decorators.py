from unittest import TestCase
from unittest.mock import patch

from api.core.exceptions import ValidationError, EntityDoesNotExist
from api.core.request_decorators import error_handler


class ErrorHandlerTests(TestCase):

    @patch('api.core.request_decorators.jsonify')
    def test_return_400_when_catchs_validation_error(self, jsonify_mock):
        jsonify_mock.return_value = {'errors': {'error': [1, 2]}}

        @error_handler
        def fn(request):
            raise ValidationError(errors={'error': [1, 2]})

        result, status_code = fn(1)

        self.assertEqual(400, status_code)
        self.assertEqual({'errors': {'error': [1, 2]}}, result)
        jsonify_mock.assert_called_with({'errors': {'error': [1, 2]}})

    @patch('api.core.request_decorators.jsonify')
    def test_return_404_when_catchs_entity_does_not_exist(self, jsonify_mock):
        user_error = {'accounts': ['User does not exists']}
        jsonify_mock.return_value = {'errors': user_error}

        @error_handler
        def fn(request):
            raise EntityDoesNotExist(errors=user_error)

        result, status_code = fn(1)

        self.assertEqual(404, status_code)
        self.assertEqual({'errors': user_error}, result)
        jsonify_mock.assert_called_with({'errors': user_error})

    @patch('api.core.request_decorators.jsonify')
    def test_return_wrapped_function_result(self, jsonify_mock):
        user_error = {'accounts': ['User does not exists']}
        jsonify_mock.return_value = {'errors': user_error}

        @error_handler
        def fn(request):
            return {'accounts': 'Yan'}, 200

        result, status_code = fn(1)

        self.assertEqual(200, status_code)
        self.assertEqual({'accounts': 'Yan'}, result)
