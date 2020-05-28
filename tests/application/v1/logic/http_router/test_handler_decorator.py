import unittest

from application.v1.logic.http_router.handler_requirements import handler_requirements
from tests.application.v1.logic.http_router import mock_data

@handler_requirements()
def handle_no_validation(request, response):
    response.body = "Hello"

@handler_requirements(required_path_parameters=['proxy'])
def handle_validation_required_path(request, response):
    response.body = "Hello"

@handler_requirements(required_path_parameters=['proxy_fail'])
def handle_validation_required_path_fail(request, response):
    response.body = "Hello"

@handler_requirements(required_headers=['x-api-key'])
def handle_validation_required_headers(request, response):
    response.body = "Hello"

@handler_requirements(required_headers=['x-api-key-fail'])
def handle_validation_required_headers_fail(request, response):
    response.body = "Hello"

@handler_requirements(required_body='v1-test-request')
def handle_validation_required_body(request, response):
    response.body = "Hello"

@handler_requirements(required_body='v1-test-request-fail')
def handle_validation_required_body_fail(request, response):
    response.body = "Hello"

class ApiGatewayHandlerDecoratorTest(unittest.TestCase):

    def test_no_authorization(self):
        response = handle_no_validation(mock_data.apigateway_event(), None)
        self.assertEqual(response['statusCode'], 200)
        self.assertEqual(response['body'],"Hello")

    def test_with_validation_require_path(self):
        response = handle_validation_required_path(mock_data.apigateway_event(), None)
        self.assertEqual(response['statusCode'], 200)
        self.assertEqual(response['body'], "Hello")

    def test_with_validation_require_path_fail(self):
        response = handle_validation_required_path_fail(mock_data.apigateway_event(), None)
        self.assertEqual(response['statusCode'], 400)

    def test_with_validation_require_headers(self):
        response = handle_validation_required_headers(mock_data.apigateway_event(), None)
        self.assertEqual(response['statusCode'], 200)
        self.assertEqual(response['body'], "Hello")

    def test_with_validation_require_headers_fail(self):
        response = handle_validation_required_headers_fail(mock_data.apigateway_event(), None)
        self.assertEqual(response['statusCode'], 400)
