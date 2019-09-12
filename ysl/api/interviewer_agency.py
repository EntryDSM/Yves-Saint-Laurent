from flask import abort
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from ysl.db import session
from ysl.db.belong import Belong
from ysl.api.interviewer import api_agency


class JoinAgency(Resource):
    @jwt_required
    def get(self):
        interviewer = get_jwt_identity()

        agency_list = session.query(Belong).filter(Belong.interviewer == interviewer).all()

        if agency_list:
            return {"agency": [
                {
                    "agency_name": agency.agency
                } for agency in agency_list]
            }, 200
        else:
            abort("None Resources", 400)


api_agency.add_resource(JoinAgency, "/agency")
