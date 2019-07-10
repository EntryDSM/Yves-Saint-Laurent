from flask import Blueprint
from flask_restful import Resource, Api

bp_test = Blueprint("test", __name__, url_prefix="/api/test")
api_test = Api(bp_test)


class Test(Resource):
    def get(self):
        return "hello"


api_test.add_resource(Test, "/1")
