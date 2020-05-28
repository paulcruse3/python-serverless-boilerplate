import importlib.util

from application.v1.logic.http_router.response_client import ResponseClient
from application.v1.logic.common import logger


class Router:

    def __init__(self, **kwargs):
        self.endpoint_base = '{}/{}'.format(kwargs['base_path'], kwargs['version'])
        self.absolute_base = kwargs['handler_path']

    def route(self, event, context):
        self.router_response = ResponseClient()
        route_results = self._route_call(event, context)
        if self.router_response.has_errors:
            return self.router_response.response
        return route_results

    def _route_call(self, event, context):
        try:
            spec = importlib.util.spec_from_file_location(self._get_import_path(event), self._get_file_path(event))
            handler_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(handler_module)
        except Exception as handler_exception:
            return self._handle_error(handler_exception, self._get_file_path(event))
        try:
            return getattr(handler_module, event['httpMethod'].lower())(event, context)
        except Exception as attr_exception:
            return self._handle_error(attr_exception, handler_module, event['httpMethod'].lower())

    def _get_import_path(self, event):
        endpoint_import = event['path'].replace('/' + self.endpoint_base + '/', '').replace('/', '_').replace('-', '_')
        return '{}.{}'.format(self.absolute_base, endpoint_import)

    def _get_file_path(self, event):
        endpoint_file = event['path'].replace('/' + self.endpoint_base + '/', '').replace('-', '_').replace('/', '_')
        if not endpoint_file:
            endpoint_file = '__init__'
        return '{}/{}.py'.format(self.absolute_base.replace('.', '/'), endpoint_file)

    def _handle_error(self, error, module=None, method=None):
        if "No such file or directory: '{}'".format(module) in str(error):
            key_path = 'url'
            code = 404
            message = 'endpoint not found'
        elif "'{}' has no attribute '{}'".format(module, method) in str(error):
            key_path = 'method'
            code = 403
            message = 'method not allowed'
        else:
            key_path = 'server'
            code = 500
            message = 'internal server error'
        self.router_response.code = code
        self.router_response.set_error(key_path, message);
        logger.log(level='ERROR', log=error, trace=True)
