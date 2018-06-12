from sqlalchemy import func, and_
from ..base.decrators import authenticated, handle_request_exception
from ..base.request import BaseHandler, JsonResponse
from common.json import json_by_result
from [module_name] import [model_name]

class [model_name]Handler(BaseHandler):
