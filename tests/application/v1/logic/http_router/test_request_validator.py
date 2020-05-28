import unittest

from application.v1.logic.http_router.request_client import RequestClient
from application.v1.logic.http_router.response_client import ResponseClient
from application.v1.logic.http_router.request_validator import RequestValidator
from tests.application.v1.logic.http_router import mock_data


class RequestValidatorTest(unittest.TestCase):

    def test_validate_headers_pass(self):
        request = RequestClient(mock_data.apigateway_event())
        response = ResponseClient()
        validator = RequestValidator(request, response)
        validator._required_fields(['test-key'], {'test-key': '123456'}, 'headers')
        self.assertFalse(response.has_errors)

    def test_validate_headers_fail(self):
        request = RequestClient(mock_data.apigateway_event())
        response = ResponseClient()
        validator = RequestValidator(request, response)
        validator._required_fields(['test-key'], {'test-key-fail': '123456'}, 'headers')
        self.assertTrue(response.has_errors)

    def test_validate_path_params_pass(self):
        request = RequestClient(mock_data.apigateway_event())
        response = ResponseClient()
        validator = RequestValidator(request, response)
        validator._required_fields(['test_path'], {'test_path': 'test_value'}, 'path parameters')
        self.assertFalse(response.has_errors)

    def test_validate_path_params_fail(self):
        request = RequestClient(mock_data.apigateway_event())
        response = ResponseClient()
        validator = RequestValidator(request, response)
        validator._required_fields(['test_path'], {'test_path_fail': 'test_value'}, 'path parameters')
        self.assertTrue(response.has_errors)
