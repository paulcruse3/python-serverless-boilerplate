import os

from application.v1.logic.http_router.router import Router

def route(event, context):
    router = Router(
        base_path=os.environ['BASE_PATH'],
        version='v1',
        handler_path='application.v1.handlers.http'
    )
    return router.route(event, context)
