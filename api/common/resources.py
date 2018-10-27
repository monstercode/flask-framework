from flask_restful import Resource
from flask_jwt_extended import jwt_required

from api.common.timeprofiler import time_profiler

class BaseResource(Resource):
    method_decorators = [time_profiler()]

# Nice to refactor: Inherit from BaseResource
class ProtectedResource(Resource):
	method_decorators = [time_profiler(), jwt_required]


