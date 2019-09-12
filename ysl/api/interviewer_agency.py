from flask import abort, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from ysl.db import session
from ysl.db.belong import Belong
from ysl.db.agency import Agency
from ysl.db.apply_interviewer import ApplyInterviewer
from ysl.api.interviewer import api_interviewer


class JoinedAgencyList(Resource):
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


class ApplyToAgency(Resource):
    @jwt_required
    def post(self):
        agency_code = request.json["agency_code"]
        interviewer = get_jwt_identity()

        agency = session.query(Agency).filter(Agency.code == agency_code).first()

        if agency:
            add_apply_interviewer = ApplyInterviewer(agency=agency_code, interviewer=interviewer)

            session.add(add_apply_interviewer)
            session.commit()
            return {"msg": "Successful apply agency"}, 200
        else:
            abort(400, " It's agency that doesn't exist.")


api_interviewer.add_resource(JoinedAgencyList, "/agency")
api_interviewer.add_resource(ApplyToAgency, "/agency/join")
