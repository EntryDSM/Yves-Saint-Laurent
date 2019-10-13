from flask import abort, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from openpyxl import Workbook


from ysl.api import check_admin
from ysl.db import session
from ysl.db.interview import Interview
from ysl.db.evaluation import Evaluation
from ysl.db.interviewer import Interviewer
from ysl.db.access import Access


class CreateExcel(Resource):
    @jwt_required
    def get(self, agency_code, interview_id):
        pass
