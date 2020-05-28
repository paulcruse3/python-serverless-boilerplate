from application.v1.logic.http_router.handler_requirements import handler_requirements
from application.v1.logic.translation import Translation

@handler_requirements(
    required_query_string_parameters=['palabra']
)
def get(request, response):
    translation = Translation(spanish=request.query_string_parameters['palabra'])
    response.body = {'translation': translation.tranlate('spanish-english')}

@handler_requirements(
    required_query_string_parameters=['palabra']
)
def delete(request, response):
    translation = Translation(spanish=request.query_string_parameters['palabra'])
    translation.remove('spanish-english');
    response.body = {'status': 'deleted'}
