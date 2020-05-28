from application.v1.logic.http_router.event_client import EventClient
from application.v1.logic.http_router.response_client import ResponseClient
from application.v1.logic.http_router.request_validator import RequestValidator

def handler_requirements(**kwargs):
    def decorator_func(func):
        def wrapper(event, context):
            request = EventClient(event)
            response = ResponseClient()
            validator = RequestValidator(request, response)
            validator.validate_request(**kwargs)
            if not response.has_errors:
                func(request, response)
            return response.response
        return wrapper
    return decorator_func
