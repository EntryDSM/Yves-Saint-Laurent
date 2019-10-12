from flask import abort, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from ysl.db import session
from ysl.db.belong import Belong
from ysl.db.agency import Agency
from ysl.db.apply_interviewer import ApplyInterviewer
from ysl.api import check_json


class JoinedAgencyList(Resource):
    @jwt_required
    def get(self):

        admin = session.query(Agency).filter(Agency.email == get_jwt_identity()).first()

        if admin:
            abort(401, "The administrator does not have a subscribed agency.")

        agencies = session.query(Belong, Agency).join(Agency).filter(Belong.interviewer == get_jwt_identity()).all()

        if agencies:
            return {"agency": [
                {
                    "agency_name": agency.Agency.name,
                    "agency_code": agency.Agency.code
                } for agency in agencies]
            }, 200
        else:
            abort("None Resources", 404)


class ApplyToAgency(Resource):
    @jwt_required
    @check_json({"agency_code": str})
    def post(self):
        agency_code = request.json["agency_code"]
        interviewer = get_jwt_identity()

        agency = session.query(Agency).filter(Agency.code == agency_code).first()

        if agency:
            apply_interviewer = session.query(ApplyInterviewer).filter(
                ApplyInterviewer.agency == agency_code).filter(ApplyInterviewer.interviewer == interviewer).first()

            if apply_interviewer:
                abort(409, "I've already applied for membership")

            else:
                add_apply_interviewer = ApplyInterviewer(agency=agency_code, interviewer=interviewer)

                session.add(add_apply_interviewer)
                session.commit()
                return {"msg": "Successful apply agency"}, 200
