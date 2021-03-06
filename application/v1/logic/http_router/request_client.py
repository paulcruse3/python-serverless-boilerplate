from application.v1.logic.common import json_helper


class RequestClient:

    def __init__(self, event):
        self._event = event

    @property
    def method(self):
        return self._event.get('httpMethod', {})

    @property
    def resource(self):
        return self._event.get('resource', {})

    @property
    def authorizer(self):
        if self._event.get('isOffline'):
            return self._event.get('headers')
        else:
            return self._event.get('requestContext', {}).get('authorizer', self._event.get('headers'))

    @property
    def headers(self):
        return self._event.get('headers', {})

    @property
    def body(self):
        return json_helper.try_decode_json(self._event.get('body', {}))

    @property
    def query_string_parameters(self):
        if self._event.get('queryStringParameters') == None:
            return {}
        return self._event.get('queryStringParameters')

    @property
    def path_parameters(self):
        return self._event.get('pathParameters', {})

    @property
    def request(self):
        return {
            'http_method': self.method,
            'resource': self.resource,
            'headers': self.headers,
            'authorizer': self.authorizer,
            'query_string_parameters': self.query_string_parameters,
            'path_parameters': self.path_parameters,
            'body': self.body
        }

    def __str__(self):
        return str({
            'request': self.request
        })
