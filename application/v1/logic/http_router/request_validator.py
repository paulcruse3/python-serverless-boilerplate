import simplejson as json
import jsonref
from jsonschema import Draft7Validator
import yaml


class RequestValidator:

    def __init__(self, RequestClient, ResponseClient):
        self.RequestClient = RequestClient
        self.ResponseClient = ResponseClient
        self._required_pairings = {
            'required_headers': 'headers',
            'required_path_parameters': 'path_parameters',
            'required_query_string_parameters': 'query_string_parameters',
            'required_body': 'body'
        }

    def validate_request(self, **kwargs):
        event = self.RequestClient.request
        for required_kwarg, event_loc in self._required_pairings.items():
            if kwargs.get(required_kwarg) and event_loc == 'body':
                self._required_body(kwargs[required_kwarg], event.get(event_loc))
            elif kwargs.get(required_kwarg):
                self._required_fields(kwargs[required_kwarg], event.get(event_loc), event_loc)

    def _required_fields(self, required=[], sent={}, list_name=''):
        missing_fields = [value for value in required if value not in sent.keys()]
        for field in missing_fields:
            self.ResponseClient.code = 400
            self.ResponseClient.set_error(list_name, 'Please provide {}'.format(field))

    def _required_body(self, schema, request_body):
        if not isinstance(request_body, dict):
            self.ResponseClient.set_error('message', 'request body is not valid JSON')
        else:
            self._check_body_for_errors(schema, request_body)

    def _check_body_for_errors(self, schema, request):
        json_schema = self._get_combined_schema(schema)
        schema_validator = Draft7Validator(json_schema)
        for schema_error in sorted(schema_validator.iter_errors(request), key=str):
            self.ResponseClient.set_error(self._get_error_path(schema_error), schema_error.message)

    def _get_combined_schema(self, schema):
        combined_schema = {}
        openapi = self._get_api_doc()
        definitions = jsonref.loads(json.dumps(openapi))['components']['schemas']
        definition_schema = definitions[schema]
        json_schemas = definition_schema['allOf'] if definition_schema.get('allOf') else [definition_schema]
        for json_schema in json_schemas:
            combined_schema.update(json_schema)
        combined_schema['additionalProperties'] = False
        return combined_schema

    def _get_error_path(self, error):
        path = '.'.join(str(path) for path in error.path)
        return path if path else 'root'

    def _get_api_doc(self):
        with open('openapi.yml') as api_doc:
            return yaml.load(api_doc, Loader=yaml.FullLoader)
