from flask import request
from flask_restful import Resource

from ysl.db.agency import Agency
from ysl.db.apply_interviewer import ApplyInterviewer
from ysl.db import session
from ysl.api import check_admin, check_json, check_agency
from ysl.api.admin import api_admin


class AgencyInformation(Resource):
    @check_admin()
    @check_agency()
    def get(self, agency_code):

        agency = session.query(Agency).filter(Agency.code == agency_code).first()

        return {
                "agency_name": agency.name,
                "agency_kind": agency.kind,
                "agency_explanation": agency.explanation,
                "agency_code": agency.code
            }, 200

    @check_admin()
    @check_agency()
    def delete(self, agency_code):

        agency = session.query(Agency).filter(Agency.code == agency_code).first()

        session.delete(agency)
        session.commit()

        return {"msg": "successful agency delete"}, 200

    @check_admin()
    @check_json({"explanation": str})
    def patch(self, agency_code):

        explanation = request.json['explanation']

        agency = session.query(Agency).filter(Agency.code == agency_code).first()
        agency.explanation = explanation

        session.commit()

        return {"msg": "successful change agency explanation"}, 200


class ApplyInterviewerList(Resource):
    @check_admin()
    @check_agency()
    def get(self, agency_code):

        interviewer_list = session.query(ApplyInterviewer).filter(ApplyInterviewer.agency == agency_code)

        return {"interviewer": [
            {
                "interviewer_name": interviewer.name
            } for interviewer in interviewer_list]
        }, 200


api_admin.add_resource(AgencyInformation, "/agency/<agency_code>")
api_admin.add_resource(ApplyInterviewer, "/<agency_code>/interviewer")