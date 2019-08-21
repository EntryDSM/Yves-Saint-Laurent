from flask import Blueprint, request, Response
from flask_restful import Resource, Api

from ysl.db.agency import Agency
from ysl.db.apply_interviewer import ApplyInterviewer
from ysl.db import db
from ysl.api import check_admin, check_json

bp_admin = Blueprint("admin", __name__, url_prefix="/api/admin")
api_admin = Api(bp_admin)


class AgencyInformation(Resource):
    @check_admin()
    def get(self):
        agency_code = request.view_args['agency_code']

        agency = Agency.query.filter_by(code=agency_code).first()

        return Response({
            "agency_name": agency.name,
            "agency_kind": agency.kind,
            "agency_explanation": agency.explanation,
            "agency_code": agency.code
        }, 200)

    @check_admin()
    def delete(self):
        agency_code = request.view_args['agency_code']

        agency = Agency.query.filter_by(code=agency_code).first()

        db.session.delete(agency)
        db.session.commit()

        return Response({"msg": "successful agency delete"}, 200)

    @check_admin()
    @check_json()
    def patch(self):
        agency_code = request.view_args['agency_code']
        explanation = request.json['explanation']

        agency = Agency.query.filter_by(code=agency_code).first()
        agency.explanation = explanation

        db.session.commit()

        return Response({"msg": "successful change agency explanation"}, 200)


class Interviewer(Resource):
    @check_admin()
    def get(self):
        agency_code = request.view_args['agency_code']

        interviewer_list = ApplyInterviewer.query.filter(ApplyInterviewer.agency == agency_code)

        return Response({"interviewer": [
            {
                "interviewer_name": interviewer.name
            } for interviewer in interviewer_list]
        }, 200)


api_admin.add_resource(Agency, "/agency/<agency_code>")
api_admin.add_resource(Interviewer, "/<agency_code>/interviewer")
