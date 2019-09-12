from flask import request, abort
from flask_restful import Resource

from ysl.db.belong import Belong
from ysl.db.apply_interviewer import ApplyInterviewer
from ysl.db import session
from ysl.api.admin import api_admin
from ysl.api import check_admin, check_json, check_agency


class AcceptInterviewer(Resource):
    @check_admin()
    @check_json({"user_email": str})
    @check_agency()
    def post(self, agency_code):
        interviewer = request.json["user_email"]

        add_interviewer = Belong(agency=agency_code, interviewer=interviewer)
        session.add(add_interviewer)

        delete_interviewer = session.query(ApplyInterviewer).filter(
            ApplyInterviewer.agency == agency_code and ApplyInterviewer.interviewer == interviewer
        ).first()

        if delete_interviewer:
            session.delete(delete_interviewer)
            session.commit()
            return {"msg": "Successful interviewer accept"}, 200
        else:
            return abort(400, "This is an interviewer who didn't apply")


class RejectInterviewer(Resource):
    @check_admin()
    @check_json({"user_email": str})
    @check_agency()
    def post(self, agency_code):
        interviewer = request.json["user_email"]

        delete_interviewer = session.query(ApplyInterviewer).filter(
            ApplyInterviewer.agency == agency_code and ApplyInterviewer.interviewer == interviewer
        ).first()

        if delete_interviewer:
            session.delete(delete_interviewer)
            session.commit()
            return {"msg": "Successful interviewer reject"}, 200
        else:
            return abort(400, "This is an interviewer who didn't apply")


api_admin.add_resource(AcceptInterviewer, "/<agency_code>/interviewer/accept")
api_admin.add_resource(RejectInterviewer, "/<agency_code>/interviewer/reject")
