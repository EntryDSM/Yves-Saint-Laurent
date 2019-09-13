from flask import abort, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from ysl.db import session
from ysl.db.access import Access
from ysl.api.admin import api_admin
from ysl.api import check_json, check_agency, check_admin


class AddAccessInterviewer(Resource):
    @jwt_required
    @check_admin()
    @check_agency()
    def get(self, interview_id):
        #join식 추가
        access_interviewer = session.query(Access).filter(Access.interview == interview_id).all()

        if access_interviewer:
            return {
                "interviewer": [
                    {
                        "interviewer": interviewer_info.name,
                        "interviewer_email": interviewer_info.email
                    } for interviewer_info in access_interviewer]
            }
        else:
            abort(400, "None interviewer")

    @jwt_required
    @check_admin()
    @check_agency()
    @check_json({"interviewer": str})
    def post(self, interview_id):
        interviewer = request.json["interviewer"]

        add_access_interviewer = Access(interview=interview_id, interviewer=interviewer)

        session.add(add_access_interviewer)
        session.commit()

        return {"msg": "Successful interviewer access"}

    @jwt_required
    @check_admin()
    @check_agency()
    def delete(self, interview_id):
        interviewer = request.args.get('interviewer')

        access_interviewer = session.query(Access).filter(
            Access.interview == interview_id and Access.interviewer == interviewer).first()

        if access_interviewer:
            session.delete(access_interviewer)
            session.commit()
            return {"msg": "Successful delete access interviewer"}
        else:
            abort(400, "None interviewer")


api_admin.add_resource(AddAccessInterviewer, "/{agency_code}/{interview_id}/access")
