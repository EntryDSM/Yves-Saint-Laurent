from flask import request, Response
from flask_restful import Resource

from ysl.db.belong import Belong
from ysl.db.apply_interviewer import ApplyInterviewer
from ysl.db import db
from ysl.api.admin import api_admin


class AcceptInterviewer(Resource):
    def post(self):
        agency_code = request.view_args['agency_code']
        interviewer = request.json['user_email']

        add_interviewer = Belong(agency=agency_code, interviewer=interviewer)
        db.session.add(add_interviewer)

        delete_interviewer = ApplyInterviewer.query.filter_by(
            ApplyInterviewer.agency == agency_code
            and ApplyInterviewer.interviewer == interviewer
        ).first()
        db.session.delete(delete_interviewer)

        db.session.commit()

        return Response({"msg": "Successful interviewer accept"}, 200)


class RejectInterviewer(Resource):
    def post(self):
        agency_code = request.view_args['agency_code']
        interviewer = request.json['user_email']

        delete_interviewer = ApplyInterviewer.query.filter_by(
            ApplyInterviewer.agency == agency_code
            and ApplyInterviewer.interviewer == interviewer
        ).first()
        db.session.delete(delete_interviewer)

        db.session.commit()

        return Response({"msg": "Successful interviewer reject"}, 200)


api_admin.add_resource(AcceptInterviewer, "/<agency_code>/interviewer/accept")
api_admin.add_resource(RejectInterviewer, "/<agency_code>/interviewer/reject")
