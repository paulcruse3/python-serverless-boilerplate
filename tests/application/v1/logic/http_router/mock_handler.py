from application.v1.logic.http_router.handler_requirements import handler_requirements

@handler_requirements()
def get(request, response):
    response.body = {
        'hello': 'world'
    }
