from flask import Blueprint, request, abort
from flask_restful import Resource, Api

from ysl.db import session
from ysl.db.agency import Agency

bp_agency = Blueprint("agency", __name__, url_prefix="/api/agency")
api_agency = Api(bp_agency)


class CheckAgencyCode(Resource):
    def get(self):
        agency_code = request.args.get('code')

        agency = session.query(Agency).filter(Agency.code == agency_code).first()

        if agency:
            return {"agency_name": agency.name,
                    "agency_explanation": agency.explanation}, 200
        else:
            return abort(400, "unseen agency")


api_agency.add_resource(CheckAgencyCode, "/check")
