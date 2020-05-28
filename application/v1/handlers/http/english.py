from application.v1.logic.http_router.handler_requirements import handler_requirements
from application.v1.logic.translation import Translation

@handler_requirements(
    required_query_string_parameters=['word']
)
def get(request, response):
    translation = Translation(english=request.query_string_parameters['word'])
    response.body = {'translation': translation.tranlate('english-spanish')}

@handler_requirements(
    required_query_string_parameters=['word']
)
def delete(request, response):
    translation = Translation(english=request.query_string_parameters['word'])
    translation.remove('english-spanish')
    response.body = {'status': 'deleted'}
